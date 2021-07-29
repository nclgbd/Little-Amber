#!/bin/sh
cd Little-Amber/
forever stopall
git commit -am "Syncing Library"
git pull origin master
forever start -c python3 scripts/main.py
