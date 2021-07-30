#!/bin/sh
forever stopall
git add .
message=$(git status)
git commit -m "${message}"
git push
forever start -c python3 scripts/main.py