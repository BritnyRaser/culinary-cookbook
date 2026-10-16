import unittest
from pathlib import Path

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
            [1, 2],
        )

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


if __name__ == "__main__":
    unittest.main()
