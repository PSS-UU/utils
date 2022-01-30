#!/bin/zsh


TEAMS=()
JUNK_FILES="*.ttf,*.bin,*.lock,*.json,*.save,*.jar,*.plist,*.xc*,*.properties,*.pbxproj"
PERTINENT_FILES="*.gradle,*.kt,*.js,*.ex,*.exs,*.swift,*.py,*.sqlite,*.dart,*.bzl,*.ts,*.tsx,*.java"


rm -rf work
mkdir work

for team in $TEAMS[@];
do
    echo "== ${team} =="
    target_dir="work/${team}"
    git clone --quiet "git@github.com:PSS-UU/${team}.git" $target_dir
    pushd $target_dir
    git fame \
        --hide-progressbar \
        --whitespace \
        --by-type \
        --format=csv \
        --include=$PERTINENT_FILES
    echo "=========="
    popd
done


