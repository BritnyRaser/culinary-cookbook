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

Preheat oven to 400°F.

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
- On Windows, press **Windows key + . (period)** to open the symbols panel.
  Select **Symbols** to insert the degree symbol (`°`) in temperatures such as
  `425°F`.

The site recognizes `.png`, `.jpg`, `.jpeg`, `.svg`, `.webp`, and `.gif` images.
Underscores are also accepted in place of hyphens in image filenames. After
adding or removing recipe files under either source folder, do these steps
before committing:

1. Run the builder from the repository root. In Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe build_recipes.py
```

   In Git Bash or WSL, run `bash build.sh`. If Python is on your `PATH`, you
   can also run `python build_recipes.py` from PowerShell.
2. Check the printed recipe count and category tree. Review the generated
   changes under `content/` and `data/`; do not edit those generated files
   directly. A category disappears when no recipes remain in its folder or
   subfolders.
3. Commit the recipe and image changes along with the intended generated
   changes, then push to `main` to deploy the site.

## VS Code recipe marker colors
The repository includes a small VS Code grammar and workspace colors for
recipe Markdown: ingredient markers (`@`) are blue, cookware markers (`#`) are
red, and timers (`~{...}`) are green. The colors match the recipe page. Only
well-formed markers are colored, so typos and incomplete markers remain
unhighlighted. The grammar does not replace the recipe build's validation.

VS Code does not automatically load extensions stored in a repository. Make
sure `extensions/culinary-recipe-markers/culinary-recipe-markers-0.1.0.vsix`
is committed to the repository so it is available after cloning, then install
it once:

1. In VS Code, open the Extensions view with **Ctrl+Shift+X**.
2. Select the **...** menu in the Extensions view and choose
   **Install from VSIX...**.
3. In the file picker, open the cloned repository's
   `extensions/culinary-recipe-markers/` folder and select
   `culinary-recipe-markers-0.1.0.vsix`.
4. Reload the VS Code window if prompted.

If the VSIX is missing, Windows users can create it from the repository root
without npm by running
`powershell -NoProfile -ExecutionPolicy Bypass -File .\extensions\culinary-recipe-markers\package.ps1`.
Then repeat the install steps above.

Alternatively, from the repository root, run
`code --install-extension extensions/culinary-recipe-markers/culinary-recipe-markers-0.1.0.vsix`.

The workspace color settings are in `.vscode/settings.json`; the grammar is in
`extensions/culinary-recipe-markers/`. The included `package.ps1` uses only
Windows PowerShell and .NET; alternatively, if you already have `vsce`, you
can run `vsce package` from the extension directory.

## VS Code spelling checks

For spelling checks while writing recipes, install the
[Code Spell Checker extension](https://marketplace.visualstudio.com/items?itemName=streetsidesoftware.code-spell-checker).
It checks Markdown as you type and underlines possible misspellings. Add
recipe-specific terms to its dictionary when they are flagged incorrectly.

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
