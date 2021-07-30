#!/bin/sh
cd Little-Amber/ || return
forever stopall
message=$(git status)
git commit -am "${message}"
forever start -c python3 scripts/main.py