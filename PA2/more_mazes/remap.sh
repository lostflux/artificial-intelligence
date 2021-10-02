#!/usr/bin/env bash

# Script to refactor Maps!

if [[ $# -ne 1 ]]; then
  echo .&2 "Usage: $0 <map_file>"
  exit 1
fi

if [[ ! -r $1 ]]; then
  echo >&2 "Error: $1 is not readable"
  exit 1
fi

function unhash() {
  perl -pe 's/('\#'*)/"." x length($1)/gei' "$1"
}

function rehash() {
  # Rehash the map

  perl -pe 's/(\-*)/"#" x length($1)/gei' "$1" |
  perl -pe 's/(\+*)/"#" x length($1)/gei' |
  perl -pe 's/(\|*)/"#" x length($1)/gei'
}

name=$(basename "$1")

unhash "$1" > "$name.tmp"

rehash "$name.tmp" > "$name.maz"

rm -f "$name.tmp"