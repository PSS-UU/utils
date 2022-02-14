#!/bin/zsh


TEAMS=("vegify-1")
JUNK_FILES="\.ttf$|\.bin$|\.lock$|\.json$|\.save$|\.jar$|\.plist$|\.xc$|\.properties$|\.pbxproj$"
PERTINENT_FILES="\.gradle$|\.kt$|\.js$|\.ex$|\.exs$|\.swift$|\.py$|\.sqlite$|\.dart$|\.bzl$|\.ts$|\.tsx$|\.java$"

rm -rf work
mkdir work

for team in $TEAMS[@];
do
    echo "== ${team} =="
    target_dir="work/${team}"
    git clone --quiet "git@github.com:PSS-UU/${team}.git" $target_dir
    pushd $target_dir
    git fame \
        --silent-progress \
        --ignore-whitespace \
        --bytype \
        --incl=$PERTINENT_FILES \
        --excl=$JUNK_FILES \
        --format=csv
    echo "=========="
    popd
done

