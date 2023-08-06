#!/bin/bash

BRANCH="origin/develop"
DIR="."
FILE=""
RELEASE=

usage() {
    echo "Usage: project_in_rc.sh [-d DIRECTORY] -r RELEASE -f FILE"
    exit 0
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--branch) BRANCH="$2"; shift 2 ;;
        -r|--release) RELEASE="$2"; shift 2 ;;
        -f|--file) FILE="$2"; shift 2 ;;
        -d|--directory) DIR="${2%/}"; shift 2 ;;
        *) echo Unkown option $1; usage ;;
    esac
done

if [[ -z ${FILE} ]]; then
    usage
fi


echo Branch       : "${BRANCH}"
echo Release      : "${RELEASE}"
echo In directory : "${DIR}"
echo Based on     : "${FILE}"
echo 


# Find sprint start
if [[ $RELEASE ]]; then
    for d in $(ls $DIR); do 
        GITDIR="$DIR/$d"

        [ -d "$GITDIR" ] || continue
        [ -d "$GITDIR/.git/" ] || continue

        git -C $GITDIR fetch &> /dev/null

        START=$(git -C $GITDIR log --grep="updating poms for ${RELEASE}-SNAPSHOT
        development" --date=short --pretty=format:'%ad' | cat - | grep "[0-9-]*" -o)
        if [[ $START ]]; then
            break
        fi
    done
    echo "  Starting at :${START}"
fi



# Message pattern from git-flow
p1="update pom dependencies for production"
p2="Updating develop poms back to pre merge state"
p3="updating develop poms to master versions to avoid merge conflicts"
p4="updating poms for branch'.*' with non-snapshot versions"
p5="updating poms for .*-SNAPSHOT development"

already_add=""
to_add=""
declare -A log

# Find project in RC
for d in $(ls $DIR); do 
    GITDIR="$DIR/$d"

    [ -d "$GITDIR" ] || continue
    [ -d "$GITDIR/.git/" ] || continue
    echo "      Process $d"

    git -C $GITDIR fetch &> /dev/null

    if [[ -z $RELEASE ]]; then
        START=$(git -C $GITDIR log --grep="updating poms for [0-9.]*-SNAPSHOT development" --date=short --pretty=format:'%ad' | cat - | grep "[0-9-]*" -o | head -1)
    fi

    echo "          at ${START}"

    RES=$(git -C $GITDIR log --since "${START}" ${BRANCH} ^origin/master --no-merges \
    --grep="${p1}" --grep="${p2}" --grep="${p3}" --grep="${p4}" --grep="${p5}" \
    --grep=".*(cherry picked from commit .*).*" --grep="DUMMY.*" \
    --invert-grep --pretty="%h%x09%ad%x09%s" --date=short | cat)

    if [[ $RES ]]; then
        if grep -Fxq "$d" $FILE; then
            already_add="$already_add $d"
        else
            to_add="$to_add $d"
            log["$d"]=$RES
        fi
    fi
done

echo "  done."
echo 


echo "  Summary"
echo "  ======="

echo '  Useless project add:'
for i in $(<$FILE); do
    if [[ ! "$already_add" =~ "$i" ]]; then
        echo "      $i"
    fi
done
echo ''


echo '  Project already add:'
for i in $already_add; do
    echo "      $i"
done
echo ''

echo '  Project to add:'
for i in $to_add; do
    echo "      $i :"
    while read -r line; do
        echo "          $line"
    done <<< "${log[$i]}"
done






