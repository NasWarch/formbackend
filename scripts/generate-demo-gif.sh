#!/usr/bin/env bash
# Generate the FormBackend demo GIF
# Prerequisites: asciinema >= 2.6, agg >= 1.4
#
# Usage: ./scripts/generate-demo-gif.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT="${1:-$PROJECT_DIR/.github/images/formbackend-demo.gif}"

# Generate the asciicast file using Python
python3 "$SCRIPT_DIR/generate-demo-cast.py"

# Convert to GIF with agg
agg \
  --cols 90 \
  --rows 24 \
  --font-family "JetBrains Mono,Fira Code,SF Mono,Menlo,Consolas,DejaVu Sans Mono" \
  --font-size 14 \
  --theme "monokai" \
  --fps-cap 20 \
  --speed 1.5 \
  --no-loop \
  /tmp/formbackend-demo.cast \
  "$OUTPUT"

echo "Done! GIF written to $OUTPUT"
