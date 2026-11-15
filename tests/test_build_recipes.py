import json
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import build_recipes
from build_recipes import RecipeParseError, parse_recipe


class ParseRecipeTests(unittest.TestCase):
    def test_parses_metadata_markers_and_notes(self):
        recipe = parse_recipe(
            """---
Title: Demo
Tags: Test
---

Mix @Flour{2 cups} in a #large bowl{} for ~{5 minutes}.
- Add @Salt{}.

Notes: Serve warm.
1. Keep leftovers covered.
""",
            Path("demo.md"),
        )

        self.assertEqual(recipe["metadata"]["map"]["Title"], "Demo")
        self.assertEqual(recipe["metadata"]["map"]["Note"], "Serve warm. Keep leftovers covered.")
        self.assertEqual([item["name"] for item in recipe["ingredients"]], ["Flour", "Salt"])
        self.assertEqual(recipe["ingredients"][0]["quantity"]["value"]["value"], "2 cups")
        self.assertEqual(recipe["cookware"][0]["name"], "large bowl")
        self.assertEqual(recipe["timers"][0]["quantity"]["value"]["value"], "5 minutes")
        self.assertEqual(
            [step["value"]["number"] for section in recipe["sections"] for step in section["content"]],
            [1],
        )
        step = recipe["sections"][0]["content"][0]
        self.assertEqual(
            [block["type"] for block in step["value"]["blocks"]],
            ["paragraph", "bullet_list"],
        )

    def test_blank_lines_separate_steps_and_dashes_render_as_bullets(self):
        recipe = parse_recipe(
            """---
Title: Demo
---

Step one.

Step two.

Mix together:
- @Cream Cheese{8 oz}
- @Milk{2 cups}
- @Vanilla{2 teaspoons}
Set aside.

Step four.
""",
            Path("demo.md"),
        )

        steps = recipe["sections"][0]["content"]
        self.assertEqual([step["value"]["number"] for step in steps], [1, 2, 3, 4])
        self.assertEqual(
            [block["type"] for block in steps[2]["value"]["blocks"]],
            ["paragraph", "bullet_list", "paragraph"],
        )
        self.assertEqual(len(steps[2]["value"]["blocks"][1]["items"]), 3)

    def test_marker_without_quantity_stops_at_next_word(self):
        recipe = parse_recipe(
            "---\nTitle: Demo\n---\n\nSpread @Jam on one side, then add @Bread Slice{2}.",
            Path("demo.md"),
        )

        self.assertEqual([item["name"] for item in recipe["ingredients"]], ["Jam", "Bread Slice"])
        self.assertEqual(recipe["ingredients"][1]["quantity"]["value"]["value"], "2")

    def test_braced_ingredient_name_can_contain_commas(self):
        recipe = parse_recipe(
            "---\nTitle: Demo\n---\n\nMix @Wheat, Rice, Corn Chex Cereal{10 cups}.",
            Path("demo.md"),
        )

        self.assertEqual(recipe["ingredients"][0]["name"], "Wheat, Rice, Corn Chex Cereal")

    def test_rejects_unterminated_marker(self):
        with self.assertRaisesRegex(RecipeParseError, "unterminated @ marker"):
            parse_recipe("---\nTitle: Demo\n---\n\nUse @Flour{2 cups.", Path("demo.md"))


class BuildRecipesTests(unittest.TestCase):
    def test_builds_new_subcategory_into_parent_index_on_first_build(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            recipes_dir = root / "recipes"
            toggle_recipes_dir = root / "recipes_toggle"
            nested_recipe = recipes_dir / "nom-nom-central" / "soup" / "venison_stew.md"
            nested_recipe.parent.mkdir(parents=True)
            nested_recipe.write_text("---\nTitle: Venison Stew\n---\n\nCook.\n", encoding="utf-8")

            data_dir = root / "data" / "recipes"
            toggle_categories_file = root / "data" / "toggle_categories.json"
            content_recipes_dir = root / "content" / "recipes"
            categories_dir = root / "content" / "categories"
            output = StringIO()
            with patch.multiple(
                build_recipes,
                ROOT=root,
                RECIPES_DIR=recipes_dir,
                TOGGLE_RECIPES_DIR=toggle_recipes_dir,
                DATA_DIR=data_dir,
                TOGGLE_CATEGORIES_FILE=toggle_categories_file,
                CONTENT_RECIPES_DIR=content_recipes_dir,
                CATEGORIES_DIR=categories_dir,
            ), redirect_stdout(output):
                self.assertEqual(build_recipes.build(), 1)

            parent_index = categories_dir / "nom-nom-central" / "_index.md"
            self.assertIn('  - "Soup"', parent_index.read_text(encoding="utf-8"))
            self.assertIn("Categories and subcategories:", output.getvalue())
            self.assertIn("- Nom Nom Central", output.getvalue())
            self.assertIn("  - Soup", output.getvalue())

    def test_removes_subcategory_after_its_last_recipe_is_deleted(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            recipes_dir = root / "recipes"
            toggle_recipes_dir = root / "recipes_toggle"
            soup_recipe = recipes_dir / "nom-nom-central" / "soup" / "venison_stew.md"
            beef_recipe = recipes_dir / "nom-nom-central" / "beef" / "roast.md"
            soup_recipe.parent.mkdir(parents=True)
            beef_recipe.parent.mkdir(parents=True)
            recipe_contents = "---\nTitle: Demo\n---\n\nCook.\n"
            soup_recipe.write_text(recipe_contents, encoding="utf-8")
            beef_recipe.write_text(recipe_contents, encoding="utf-8")

            data_dir = root / "data" / "recipes"
            toggle_categories_file = root / "data" / "toggle_categories.json"
            content_recipes_dir = root / "content" / "recipes"
            categories_dir = root / "content" / "categories"
            with patch.multiple(
                build_recipes,
                ROOT=root,
                RECIPES_DIR=recipes_dir,
                TOGGLE_RECIPES_DIR=toggle_recipes_dir,
                DATA_DIR=data_dir,
                TOGGLE_CATEGORIES_FILE=toggle_categories_file,
                CONTENT_RECIPES_DIR=content_recipes_dir,
                CATEGORIES_DIR=categories_dir,
            ):
                build_recipes.build()
                soup_recipe.unlink()
                self.assertEqual(build_recipes.build(), 1)

            parent_index = categories_dir / "nom-nom-central" / "_index.md"
            self.assertNotIn("Soup", parent_index.read_text(encoding="utf-8"))
            self.assertFalse((categories_dir / "nom-nom-central" / "soup").exists())

    def test_builds_toggle_recipes_and_records_their_category_roots(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            recipes_dir = root / "recipes"
            toggle_recipes_dir = root / "recipes_toggle"
            toggle_recipe = toggle_recipes_dir / "pawlickin'-treats" / "bird_feet.md"
            nested_recipe = (
                toggle_recipes_dir
                / "pawlickin'-treats"
                / "bird-snacks"
                / "dehydrated_treats.md"
            )
            recipe_contents = "---\nTitle: Toggle Recipe\n---\n\nCook.\n"
            toggle_recipe.parent.mkdir(parents=True)
            nested_recipe.parent.mkdir(parents=True)
            toggle_recipe.write_text(recipe_contents, encoding="utf-8")
            nested_recipe.write_text(recipe_contents, encoding="utf-8")

            data_dir = root / "data" / "recipes"
            toggle_categories_file = root / "data" / "toggle_categories.json"
            content_recipes_dir = root / "content" / "recipes"
            categories_dir = root / "content" / "categories"
            with patch.multiple(
                build_recipes,
                ROOT=root,
                RECIPES_DIR=recipes_dir,
                TOGGLE_RECIPES_DIR=toggle_recipes_dir,
                DATA_DIR=data_dir,
                TOGGLE_CATEGORIES_FILE=toggle_categories_file,
                CONTENT_RECIPES_DIR=content_recipes_dir,
                CATEGORIES_DIR=categories_dir,
            ):
                self.assertEqual(build_recipes.build(), 2)

            self.assertEqual(
                json.loads(toggle_categories_file.read_text(encoding="utf-8")),
                ["Pawlickin' Treats"],
            )
            self.assertTrue(
                (
                    content_recipes_dir
                    / "pawlickin'-treats"
                    / "bird-snacks"
                    / "dehydrated_treats.md"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()
