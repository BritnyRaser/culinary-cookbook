#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if ! command -v inotifywait >/dev/null 2>&1; then
  echo "inotifywait is required for automatic watching. Install inotify-tools and rerun this script."
  exit 1
fi

./build.sh
hugo --quiet

echo "Watching recipes/ and static/ for changes..."
while true; do
  inotifywait -rq -e modify,create,delete,move --format '%w%f' recipes static |
    while IFS= read -r changed; do
      [ -n "$changed" ] || continue
      echo "Detected change: $changed"
      ./build.sh
      hugo --quiet
    done
done
