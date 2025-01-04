#!/usr/bin/env bash

textx generate src/cronspell/cronspell.tx --target PlantUML --overwrite

textx generate src/cronspell/cronspell.tx --target dot --overwrite
plantuml src/cronspell/cronspell.pu -tsvg -Smonochrome=true

python docs/scripts/generate_docs.py
