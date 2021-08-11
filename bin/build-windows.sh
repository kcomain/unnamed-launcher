#!/bin/bash

#export PS4='[$0 L$LINENO]++ '
#set -x
set -e
# keep track of the last executed command
# shellcheck disable=SC2154
trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
# echo an error message before exiting
# shellcheck disable=SC2154
trap 'echo "\"${last_command}\" command filed with exit code $?."' EXIT

export WINEDEBUG=-all

# check if wine exists
printf 'checking if wine exists... '
if ! command -v wine &> /dev/null; then
    echo 'no'
    echo 'since wine is not found, not building windows binary.'
    exit 0
fi
echo 'yes'

#echo "current directory is $(pwd)"
#printf "creating temporary directory... "
#mkdir -p temp
#echo 'done'

printf "setting wineprefix... "
export WINEPREFIX="$PWD/temp"
export WINEARCH=win64
echo "$WINEPREFIX on $WINEARCH"

printf "winebooting temp directory... "
wine wineboot &>/dev/null
echo "done"

printf "checking if requirements.txt exists... "
if ! [ -f requirements.txt ]; then
    printf "no, generating... "
    # shellcheck disable=SC2094
    poetry export --dev --no-hashes -f requirements.txt > requirements.txt
    echo "done"
else
    echo "yes"
fi

echo "downloading python installer (3.8.1)... "
if ! [ -e "temp/PythonInstaller.exe" ]; then
    curl -Lo temp/PythonInstaller.exe https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe -#
fi
echo "finished downloading python installer"

printf "installing python... "
wine temp/PythonInstaller.exe /passive Include_doc=0 InstallLauncherAllUsers=0 Include_tcltk=0 &>/dev/null
echo "done"

# Fails with mysterious charmap error, doesn't work on my machine so disabled.
#printf "upgrading pip... "
#wine py -m pip install --upgrade pip > /dev/null
#echo "done"

printf "installing dependencies... "
sleep 2
echo ""
wine py -m pip install --no-warn-script-location -r requirements.txt > /dev/null
