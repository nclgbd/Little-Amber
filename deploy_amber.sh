#!/bin/sh

check_fail() {
    if [ ${?} -eq 0 ]; then
        echo 0
    else
        echo 1
        return
    fi
}

forever stopall || exit 5
git add . || exit 6
message=$(git status) || exit 7
git commit -m "${message}" || exit 8
git pull || exit 9
git push || exit 10
forever start -c python3 scripts/main.py || exit 11
