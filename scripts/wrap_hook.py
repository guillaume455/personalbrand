#!/usr/bin/env python3
"""Découpe le texte du hook en lignes, une par fichier, pour drawtext."""
import os
import sys
import textwrap

hook, prefix = sys.argv[1], sys.argv[2]
width = int(os.environ.get("HOOK_MAX_CHARS", 20))
lines = textwrap.wrap(hook, width=width, break_long_words=False) or [hook]
for i, line in enumerate(lines):
    with open(f"{prefix}-{i}.txt", "w", encoding="utf-8") as f:
        f.write(line)
print(len(lines))
