# Raser-Recipes
All Recipes we use or like to try

## Building

Recipe sources live in `recipes/` as Markdown files with a metadata block and
recipe text. Ingredient markers use `@Name{amount}`, cookware markers use
`#Name{}`, and timers use `~{duration}`. Empty lines separate numbered steps;
consecutive `- ` lines render as bullets within a step. `build.sh` runs the project-owned
`build_recipes.py` parser to generate Hugo's recipe data and pages. It requires
Python 3 but no external recipe parser.
