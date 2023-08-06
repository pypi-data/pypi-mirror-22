#!/bin/bash

ERROR=""


# FUNCTIONS
# -------------------------------------------------------------

function error {
    echo Error: $1
    ERROR=$"$ERROR\n$1"
}

function die {
    echo "$ERROR"
    exit 1
}

function usage {
    echo "Usage: check_rc_finish.sh -r RELEASE -n NEXT-SNAPSHOT -f FILE [-d DIRECTORY]"
    exit 0
}

function checkProjectRc { # DIR PROJECT RELEASE RC
    GIT="$1/$2"
    [ -d "$GIT" ] || continue
    [ -d "$GIT/.git/" ] || continue
    echo "  Process $2"

    if [[ $(git -C $GIT status --porcelain) ]]; then
        echo Change to commit in $2
        exit 1
    fi

    git -C $GIT checkout develop 
    processModules $GIT $4

    git -C $GIT checkout master
    processModules $GIT $3
    
    echo "  done."
    echo 
}

function processModules { # DIR VERSION
    pattern="<module>([^\/]*)<\/module>"
    modules=$(cat "$1/pom.xml" | grep -E "<module>.*<\/module>")

    version=$(mvn -f $1/pom.xml help:evaluate -Dexpression=project.version \
        | grep -v "^\[" | grep "[0-9.-]*[-SNAPSHOT]*")

    [[ $version == $2 ]] || error "Root version ($version) not equals to $2"
    
    for line in $modules; do
       [[ $line =~ $pattern ]] || continue
        processModule $1 ${BASH_REMATCH[1]} $2
    done
}

function processModule { # DIR MODULE VERSION
    echo "    module: $2"
    version=$(mvn -f $1/pom.xml help:evaluate -Dexpression=project.version -pl $2\
        | grep -v "^\[" | grep "[0-9.-]*[-SNAPSHOT]*")
    [[ $version == $3 ]] || error "Module $2 version ($version) not equals to $3"
}

# Process
# ----------------------------------------------------------

DEV="origin/develop"
MASTER="origin/master"
DIR="."
LIST=""
RC=""
RELEASE=""


while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--release) RELEASE="$2";   shift 2 ;;
        -n|--next) RC="$2";           shift 2 ;;
        -l|--list) LIST="$2";         shift 2 ;;
        -d|--directory) DIR="${2%/}"; shift 2 ;;
        *) echo Unkown option $1; usage ;;
    esac
done

echo Check finish $RELEASE to $RC at $DIR
echo For list $LIST
echo

if [[ -z ${LIST} ]] || [[ -z $RC ]] || [[ -z RELEASE ]]; then
    usage
fi

for project_name in `echo "${LIST}" | sed "s/,/ /g"`
do
    checkProjectRc $DIR $project_name $RELEASE $RC
done

if [[ $ERROR ]]; then
    die
fi

exit 0


