#Culinary-Cookbook

## Building

Recipe sources live in `recipes/` as Markdown files with a metadata block and
recipe text.
Ingredient markers use `@Name{amount}`
cookware markers use `#Name{}`
timers use `~{duration}`
Empty lines separate numbered steps
consecutive `- ` lines render as bullets within a step
`build.sh` runs the project-owned `build_recipes.py` parser to generate Hugo's recipe data and pages. It requires
Python 3 but no external recipe parser.

## Adding categories, recipes, and pictures

### 1. Create a category

Create a folder under `recipes/`, then add at least one recipe Markdown file
inside it. The folder becomes the category; nested folders become
subcategories. For example, a recipe in `recipes/dinners/poultry/` belongs to
the `Dinners / Poultry` subcategory. The build generates category pages and
indexes from recipe folders, so an empty folder by itself will not create a
category. `Tags` in a recipe are descriptors, not categories.

For categories and recipes that should be available from the hamburger menu
but omitted from the homepage, put them under `recipes_toggle/` instead. For
example, `recipes_toggle/pawlickin'-treats/` is the Pawlickin' Treats category.
Recipes and nested categories added anywhere under that folder are built like
other recipes, but are only listed through the hamburger menu's **Category**
options, not the homepage category tiles or recipe cards. Add a Markdown recipe
inside each category folder; the folder names determine the category hierarchy.

Category names are based on their folder names (hyphens and underscores are
displayed as spaces). To add a category banner image, save it in
`static/images/website/` using the category's displayed name converted to
lowercase and hyphens. For example, use
`static/images/website/dinners.jpg` for `Dinners`. Use this same location and
naming rule for categories under `recipes_toggle/`; their image appears on the
category page banner, even though the category is not shown as a homepage tile.

### 2. Add a recipe and its picture

Create a Markdown file inside the category folder, for example
`recipes/dinners/lemon_herb_chicken.md`. The filename becomes the recipe's
unique identifier; filenames (without `.md`) must be unique across both
`recipes/` and `recipes_toggle/`.

To add the recipe picture, save it in `static/images/recipes/` using the
recipe's **Title** as the filename in lowercase with hyphens. For the example
below, use `static/images/recipes/lemon-herb-chicken.jpg`. The picture is
matched automatically by title; it does not need to be referenced in the
recipe Markdown.

### 3. Write the recipe

The first line of the Markdown file must be `---`. Put metadata between the
opening and closing `---` lines, with one `Key: value` per line. Then add the
instructions, separating steps with blank lines:

```markdown
---
Title: Lemon Herb Chicken
Servings: 4
Tags: Dinner, Poultry
Link: https://example.com/lemon-herb-chicken
---

Preheat oven to 400 degrees F.

Season @Chicken{4 breasts} with @Salt and @Pepper, then cook in a #skillet{}.
Bake for ~{20 minutes}, or until cooked through.

Notes: Alternatively, cook in an air fryer for ~{18 minutes}.
```

- **Tags** are comma-separated descriptors such as meal type, cuisine, or
  dietary style. They appear on the recipe and can be used to filter recipes
  from the homepage. Ingredient names are also included automatically from the
  recipe steps, so you do not need to repeat ingredients in `Tags`. Tags do not
  determine the recipe's category.
- **Link** is the source URL. It appears as a Source link on the recipe page,
  making it easy to revisit and credit the original recipe.
- **Notes** hold useful extra context outside the numbered instructions, such
  as substitutions or preparation tips. Put `Notes:` after the instructions;
  the note text can continue on following lines. Notes appear separately from
  the steps. A short note can also be added as `Note: Your note here` in the
  metadata.
- Mark ingredients with `@Name{amount}`, cookware with `#Name{}`, and timers
  with `~{duration}`. Amounts are optional. Empty lines separate numbered
  steps, and consecutive `- ` lines render as bullets within a step.

The site recognizes `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`, and `.gif` images.
Underscores are also accepted in place of hyphens in image filenames. Run
`build.sh` after adding a recipe under either source folder; generated pages
and category indexes under `content/` and recipe data under `data/` should not
be edited directly.

## Using the homepage

The homepage shows category tiles and recipe cards. Click a category tile to
open that category, or click a recipe title or picture to open its recipe.

- **Search by name** narrows the recipe cards as you type.
- **Filter by tags** lets you search the available recipe tags and select one
  or more. A recipe appears if it matches any selected tag. Click a selected
  tag chip to remove it. The name search and selected tags work together; if
  there are no matches, the page displays a message.

## Hamburger menu

Click the hamburger button to open or close the navigation menu. Clicking
outside the menu closes it. The **Category** button expands or collapses its
category links. The menu options are:

- **Home** returns to the homepage.
- **Category** opens a list of categories; choose one to browse its recipes.
- **Meal Plan** opens the meal planner.
- **Grocery List** opens the grocery list.

### Categories in the hamburger menu

The **Category** menu provides links to browse categories and their recipes.
To create a menu category, add a recipe Markdown file inside a new folder under
`recipes/`; nested folders create subcategories. Categories under
`recipes_toggle/` also appear in this menu, including their nested categories,
but remain hidden from the homepage. A folder needs at least one recipe for the
build to generate its category page.

Category banner images go in `static/images/website/`. Name each image to match
the category's displayed name, lowercased with hyphens between words—for
example, `recipes_toggle/pawlickin'-treats/` uses
`static/images/website/pawlickin'-treats.jpg`. Use the subcategory's own
displayed name for its banner image. Supported image extensions and underscore
filenames are listed above.
