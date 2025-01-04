#!/usr/bin/env bash

textx generate src/cronspell/cronspell.tx --target PlantUML --overwrite

textx generate src/cronspell/cronspell.tx --target dot --overwrite
dot -O src/cronspell/cronspell.dot -Tsvg

python scripts/generate_docs.py
