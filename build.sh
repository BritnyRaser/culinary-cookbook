#!/bin/bash

# ==============================================================================
# Recipe Processing Script
# 
# 1. Scans the 'recipes/' directory for all Cooklang (.cook) files.
# 2. Uses CookCLI to parse each .cook file into a JSON data file in 'data/recipes/'.
# 3. Generates a matching Markdown (.md) file in 'content/recipes/' so Hugo 
#    creates the HTML page route for each individual recipe.
# ==============================================================================

mkdir -p data/recipes
mkdir -p content/recipes

for file in recipes/*.cook; do
  [ -f "$file" ] || continue
  filename=$(basename "$file" .cook)
  
  # CookCLI syntax to output JSON to stdout:
  cook recipe "$file" json > "data/recipes/${filename}.json"
  
  # Generate Hugo markdown content route
  cat <<EOF > "content/recipes/${filename}.md"
---
title: "${filename}"
---
EOF
done
