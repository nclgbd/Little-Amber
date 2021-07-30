#!/bin/sh
forever stopall || return 5
git add . || return 6
message=$(git status) || return 7
git commit -m "${message}" || return 8
git pull || return 9
git push || return 10
forever start -c python3 scripts/main.py || return 11