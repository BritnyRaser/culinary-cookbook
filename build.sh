#!/bin/bash
set -euo pipefail

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
mkdir -p static/images

find data/recipes -type f -name '*.json' -delete 2>/dev/null || true
find content/recipes -type f -name '*.md' -delete 2>/dev/null || true

while IFS= read -r -d '' file; do
  [ -f "$file" ] || continue

  filename=$(basename "$file" .cook)
  rel_dir=$(dirname "$file")
  rel_dir=${rel_dir#recipes/}

  recipe_output_dir="content/recipes"
  category=""

  if [ -n "$rel_dir" ] && [ "$rel_dir" != "." ] && [ "$rel_dir" != "recipes" ]; then
    recipe_output_dir="content/recipes/${rel_dir}"
    mkdir -p "$recipe_output_dir"

    category=$(python3 - "$rel_dir" <<'PY'
import sys
raw = sys.argv[1]
parts = [p.replace('_', ' ').replace('-', ' ') for p in raw.split('/') if p]
pretty = []
for part in parts:
    pretty.append(' '.join(word.capitalize() for word in part.split()))
print(' / '.join(pretty))
PY
)
  fi

  # CookCLI syntax to output JSON to stdout:
  cook recipe --format json "$file" > "data/recipes/${filename}.json"

  title=$(python3 - "data/recipes/${filename}.json" <<'PY'
import json, sys
path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
meta = data.get('metadata', {}).get('map', {})
for key in ('title', 'Title', 'TITLE'):
    value = meta.get(key)
    if value not in (None, ''):
        print(value)
        break
else:
    print('')
PY
)

  if [ -z "$title" ]; then
    title="$filename"
  fi

  escaped_title=${title//\"/\\\"}

  if [ -n "$category" ]; then
    cat <<EOF > "${recipe_output_dir}/${filename}.md"
---
title: "${escaped_title}"
categories:
  - "${category}"
---
EOF
  else
    cat <<EOF > "${recipe_output_dir}/${filename}.md"
---
title: "${escaped_title}"
---
EOF
  fi
done < <(find recipes -type f -name '*.cook' -print0)
