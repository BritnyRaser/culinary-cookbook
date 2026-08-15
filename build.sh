#!/bin/bash
set -e

# This script automatically scans your recipes/ folder, 
# translates each .cook file into JSON using CookCLI, 
# and drops the output into Hugo's data pipeline.

# Create a temporary directory for Hugo to read the transformed recipe data
mkdir -p data/recipes

# Convert every .cook file into a JSON data file for Hugo
find recipes -name "*.cook" | while read -r f; do
  slug=$(basename "$f" .cook | tr '[:upper:]' '[:lower:]' | tr ' ' '-')
  cook recipe "$f" -f json > "data/recipes/${slug}.json"
done
