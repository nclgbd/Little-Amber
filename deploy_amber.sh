#!/bin/sh

check_fail() {
    if [ ${?} -eq 0 ]; then
        echo 0
    else
        echo 1
        return
    fi
}

forever stopall
check_fail
git add .
check_fail
message=$(git status)
check_fail
git commit -m "${message}"
check_fail
git pull
check_fail
git push
check_fail
forever start -c python3 scripts/main.py
check_fail
