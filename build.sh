#!/bin/bash

# ==============================================================================
# Recipe Processing Script
# 
# 1. Scans the 'recipes/' directory for all Cooklang (.cook) files.
# 2. Uses CookCLI to parse each .cook file into a JSON data file in 'data/recipes/'.
# 3. Generates a matching Markdown (.md) file in 'content/recipes/' so Hugo 
#    creates the HTML page route for each individual recipe.
# ==============================================================================

# Create necessary directories
mkdir -p data/recipes
mkdir -p content/recipes

# Process all .cook files in the recipes/ directory
for file in recipes/*.cook; do
  [ -e "$file" ] || continue
  
  # Get base filename without extension
  filename=$(basename "$file" .cook)
  
  # 1. Convert .cook file to JSON for Hugo data usage
  cook recipe "$file" --json > "data/recipes/${filename}.json"
  
  # 2. Create a content file so Hugo generates the HTML page route
  cat <<EOF > "content/recipes/${filename}.md"
---
title: "${filename}"
recipe_key: "${filename}"
---
EOF
done
