#!/usr/bin/env python3
"""Build recipe data and Hugo pages from the cookbook's Markdown sources."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
RECIPES_DIR = ROOT / "recipes"
DATA_DIR = ROOT / "data" / "recipes"
CONTENT_RECIPES_DIR = ROOT / "content" / "recipes"
CATEGORIES_DIR = ROOT / "content" / "categories"
MARKER_END = set(",.;:!?&")


class RecipeParseError(ValueError):
    pass


def _display_name(value: str) -> str:
    return " / ".join(
        " ".join(part.replace("_", " ").replace("-", " ").split()).title()
        for part in value.split("/")
        if part
    )


def _yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _parse_header(lines: list[str], source: Path) -> tuple[dict[str, str], int]:
    if not lines or lines[0].strip() != "---":
        raise RecipeParseError(f"{source}: expected metadata between --- lines")

    metadata: dict[str, str] = {}
    for index in range(1, len(lines)):
        line = lines[index].strip()
        if line == "---":
            return metadata, index + 1
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise RecipeParseError(f"{source}:{index + 1}: expected 'Key: value'")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    raise RecipeParseError(f"{source}: metadata block is missing its closing ---")


def _marker(source: str, start: int, marker: str, line_number: int, path: Path):
    name_start = start + 1
    next_marker = min(
        (position for symbol in "@#~" if (position := source.find(symbol, name_start)) >= 0),
        default=len(source),
    )
    brace = source.find("{", name_start, next_marker)
    if brace >= 0:
        name = source[name_start:brace].strip()
        close = source.find("}", brace + 1)
        if close < 0:
            raise RecipeParseError(f"{path}:{line_number}: unterminated {marker} marker")
        return name, source[brace + 1 : close].strip(), close + 1

    end = name_start
    while end < len(source) and not source[end].isspace() and source[end] not in MARKER_END | {"@", "#", "~", "{", "}"}:
        end += 1
    return source[name_start:end].strip(), None, end


def _text_item(value: str) -> dict[str, str]:
    return {"type": "text", "value": value}


def _quantity(value: str | None) -> dict[str, Any] | None:
    if value is None:
        return None
    return {
        "value": {"type": "text", "value": value},
        "unit": None,
        "scalable": False,
    }


def _parse_inline_items(
    text: str,
    ingredients: list[dict[str, Any]],
    cookware: list[dict[str, Any]],
    timers: list[dict[str, Any]],
    line_number: int,
    source: Path,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    plain: list[str] = []

    def flush_text() -> None:
        if plain:
            items.append(_text_item("".join(plain)))
            plain.clear()

    index = 0
    while index < len(text):
        marker = text[index]
        if marker not in "@#~":
            plain.append(text[index])
            index += 1
            continue

        if marker == "~":
            if index + 1 >= len(text) or text[index + 1] != "{":
                plain.append(marker)
                index += 1
                continue
            close = text.find("}", index + 2)
            if close < 0:
                raise RecipeParseError(f"{source}:{line_number}: unterminated timer marker")
            quantity = text[index + 2 : close].strip()
            timer_index = len(timers)
            timers.append({"name": None, "quantity": _quantity(quantity)})
            flush_text()
            items.append({"type": "timer", "index": timer_index})
            index = close + 1
            continue

        name, quantity, end = _marker(text, index, marker, line_number, source)
        if not name:
            plain.append(marker)
            index += 1
            continue

        flush_text()
        if marker == "@":
            entry_index = next(
                (
                    item_index
                    for item_index, item in enumerate(ingredients)
                    if item["name"] == name and item["quantity"] == _quantity(quantity)
                ),
                -1,
            )
            if entry_index < 0:
                entry_index = len(ingredients)
                ingredients.append(
                    {
                        "name": name,
                        "alias": None,
                        "quantity": _quantity(quantity),
                        "note": None,
                        "reference": None,
                        "relation": {
                            "relation": {
                                "type": "definition",
                                "referenced_from": [],
                                "defined_in_step": True,
                            },
                            "reference_target": None,
                        },
                        "modifiers": "",
                    }
                )
            items.append({"type": "ingredient", "index": entry_index})
        else:
            entry_index = next(
                (item_index for item_index, item in enumerate(cookware) if item["name"] == name),
                -1,
            )
            if entry_index < 0:
                entry_index = len(cookware)
                cookware.append(
                    {
                        "name": name,
                        "alias": None,
                        "quantity": _quantity(quantity),
                        "note": None,
                        "relation": {
                            "type": "definition",
                            "referenced_from": [],
                            "defined_in_step": True,
                        },
                        "modifiers": "",
                    }
                )
            items.append({"type": "cookware", "index": entry_index})
        index = end

    flush_text()
    return items


def _is_bullet(line: str) -> bool:
    return line.lstrip().startswith(("- ", "* "))


def _parse_step(
    lines: list[tuple[int, str]],
    ingredients: list[dict[str, Any]],
    cookware: list[dict[str, Any]],
    timers: list[dict[str, Any]],
    source: Path,
) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    paragraph: list[tuple[int, str]] = []
    bullets: list[list[dict[str, Any]]] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(line.strip() for _, line in paragraph)
            items = _parse_inline_items(
                text, ingredients, cookware, timers, paragraph[0][0], source
            )
            if items:
                blocks.append({"type": "paragraph", "items": items})
            paragraph.clear()

    def flush_bullets() -> None:
        if bullets:
            blocks.append({"type": "bullet_list", "items": bullets.copy()})
            bullets.clear()

    for line_number, line in lines:
        stripped = line.strip()
        if _is_bullet(stripped):
            flush_paragraph()
            bullets.append(
                _parse_inline_items(
                    stripped[2:].strip(),
                    ingredients,
                    cookware,
                    timers,
                    line_number,
                    source,
                )
            )
        else:
            flush_bullets()
            paragraph.append((line_number, line))

    flush_paragraph()
    flush_bullets()
    return {"type": "step", "value": {"blocks": blocks, "number": 0}}


def parse_recipe(contents: str, source: Path) -> dict[str, Any]:
    lines = contents.splitlines()
    metadata, body_start = _parse_header(lines, source)
    ingredients: list[dict[str, Any]] = []
    cookware: list[dict[str, Any]] = []
    timers: list[dict[str, Any]] = []
    steps: list[dict[str, Any]] = []
    note_lines: list[str] = []
    in_notes = False
    step_lines: list[tuple[int, str]] = []

    def flush_step() -> None:
        if step_lines:
            step = _parse_step(step_lines, ingredients, cookware, timers, source)
            if step["value"]["blocks"]:
                steps.append(step)
            step_lines.clear()

    for line_number, raw_line in enumerate(lines[body_start:], body_start + 1):
        stripped = raw_line.strip()
        note_match = re.match(r"^Notes:\s*(.*)$", stripped, flags=re.IGNORECASE)
        if note_match:
            flush_step()
            in_notes = True
            if note_match.group(1):
                note_lines.append(note_match.group(1))
            continue
        if in_notes:
            if stripped:
                note_lines.append(re.sub(r"^\d+\.\s*", "", stripped))
            continue
        if not stripped:
            flush_step()
        else:
            step_lines.append((line_number, raw_line))
    flush_step()

    if note_lines:
        metadata.setdefault("Note", " ".join(note_lines))
    if "Notes" in metadata:
        metadata.setdefault("Note", metadata.pop("Notes"))

    for number, step in enumerate(steps, start=1):
        step["value"]["number"] = number

    return {
        "metadata": {"map": metadata},
        "sections": [{"name": None, "content": steps}],
        "ingredients": ingredients,
        "cookware": cookware,
        "timers": timers,
        "inline_quantities": [],
    }


def _recipe_title(data: dict[str, Any], fallback: str) -> str:
    metadata = data["metadata"]["map"]
    for key, value in metadata.items():
        if key.lower() == "title" and value:
            return value
    return fallback


def _write_recipe_page(path: Path, title: str, categories: list[str]) -> None:
    content = ["---", f"title: {_yaml_string(title)}"]
    if categories:
        content.append("categories:")
        content.extend(f"  - {_yaml_string(category)}" for category in categories)
    content.append("---")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(content) + "\n", encoding="utf-8")


def _write_category_indexes(recipe_directories: set[Path]) -> None:
    for relative_dir in sorted(recipe_directories, key=lambda item: (len(item.parts), str(item))):
        directory = CATEGORIES_DIR / relative_dir
        directory.mkdir(parents=True, exist_ok=True)
        title = _display_name(relative_dir.name)
        child_directories = sorted(
            (child for child in directory.iterdir() if child.is_dir()),
            key=lambda child: _display_name(child.name).casefold(),
        )
        content = ["---", f"title: {_yaml_string(title)}"]
        if child_directories:
            content.append("subcategories:")
            content.extend(
                f"  - {_yaml_string(_display_name(child.name))}"
                for child in child_directories
            )
        content.append("---")
        (directory / "_index.md").write_text("\n".join(content) + "\n", encoding="utf-8")


def build() -> int:
    recipe_files = sorted(RECIPES_DIR.rglob("*.md"))
    if not recipe_files:
        raise RuntimeError(f"No Markdown recipes found in {RECIPES_DIR}")

    parsed_recipes: list[tuple[Path, Path, dict[str, Any]]] = []
    output_names: set[str] = set()
    for source in recipe_files:
        if source.stem in output_names:
            raise RuntimeError(f"Recipe filenames must be unique: {source.stem}")
        output_names.add(source.stem)
        relative = source.relative_to(RECIPES_DIR)
        data = parse_recipe(source.read_text(encoding="utf-8"), source)
        parsed_recipes.append((source, relative, data))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_RECIPES_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "static" / "images").mkdir(parents=True, exist_ok=True)

    for generated in DATA_DIR.glob("*.json"):
        generated.unlink()
    for generated in CONTENT_RECIPES_DIR.rglob("*.md"):
        generated.unlink()

    recipe_directories: set[Path] = set()
    for source, relative, data in parsed_recipes:
        category_path = relative.parent
        json_path = DATA_DIR / f"{source.stem}.json"
        json_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        categories = [_display_name(part) for part in category_path.parts if part != "."]
        category = " / ".join(categories)
        page_path = CONTENT_RECIPES_DIR / category_path / f"{source.stem}.md"
        _write_recipe_page(
            page_path,
            _recipe_title(data, source.stem),
            [category] if category else [],
        )
        for depth in range(1, len(category_path.parts) + 1):
            recipe_directories.add(Path(*category_path.parts[:depth]))

    _write_category_indexes(recipe_directories)
    print(f"Processed {len(recipe_files)} recipes.")
    return len(recipe_files)


if __name__ == "__main__":
    try:
        build()
    except (OSError, RecipeParseError, RuntimeError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
