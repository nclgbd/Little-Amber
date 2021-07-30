#!/bin/sh
forever stopall || exit 6
git add . || exit 7
message=$(git status) || exit 8
git commit -m "${message}" || exit 9
git pull || exit 10
git push || exit 11
forever start -c python3 scripts/main.py || exit 12
