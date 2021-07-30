#!/bin/sh
forever stopall
message=$(git status)
git commit -am "${message}"
git push
forever start -c python3 scripts/main.py