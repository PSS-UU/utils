#!/bin/zsh
set -o pipefail
set -o errexit
set -o nounset
set -x

TEAMS=(whoami pixelice mealmayham stickling mibrary ting the-final-rest)

for team in $TEAMS[@];
do
    ../.venv/bin/python3 burndown.py ${team} ${team}-burndown.png > ${team}.tickets
done
