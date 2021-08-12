#!/bin/bash
echo "this script is deprecated as this does not work properly with wine. if you're on windows, try the bat script instead."
echo "why this didn't work? see this https://cdn.discordapp.com/attachments/680402823040860199/875143264443977738/unknown.png"
exit 1

#
##export PS4='[$0 L$LINENO]++ '
##set -x
#set -e
## keep track of the last executed command
## shellcheck disable=SC2154
#trap 'last_command=$current_command; current_command=$BASH_COMMAND' DEBUG
## echo an error message before exiting
## shellcheck disable=SC2154
#trap 'echo "\"${last_command}\" command ended with exit code $?."' EXIT
#
#export WINEDEBUG=-all
#
## check if wine exists
#printf 'checking if wine exists... '
#if ! command -v wine &> /dev/null; then
#    echo 'no'
#    echo 'since wine is not found, not building windows binary.'
#    exit 0
#fi
#echo 'yes'
#
##echo "current directory is $(pwd)"
##printf "creating temporary directory... "
##mkdir -p temp
##echo 'done'
#
#printf "setting wineprefix... "
#export WINEPREFIX="$PWD/temp"
#export WINEARCH=win64
#echo "$WINEPREFIX on $WINEARCH"
#
#printf "winebooting temp directory... "
#wine wineboot &>/dev/null
#echo "done"
#
#printf "removing previous build directory... "
#if [ -d build/unnamed-launcher ]; then
#    rm -fr build/unnamed-launcher
#    echo "done"
#else
#    echo "doesn't exist"
#fi
#
#printf "checking if requirements.txt exists... "
#if ! [ -f requirements.txt ]; then
#    printf "no, generating... "
#    # shellcheck disable=SC2094
#    poetry export --dev --without-hashes -f requirements.txt > requirements.txt
#    echo "done"
#else
#    echo "yes"
#fi
#
#echo "downloading python installer (3.8.1)... "
#if ! [ -e "temp/PythonInstaller.exe" ]; then
#    curl -Lo temp/PythonInstaller.exe https://www.python.org/ftp/python/3.8.1/python-3.8.1-amd64.exe -#
#fi
#echo "finished downloading python installer"
#
#printf "installing python... "
#wine temp/PythonInstaller.exe /passive Include_doc=0 InstallLauncherAllUsers=0 Include_tcltk=0 &>/dev/null
#echo "done"
#
## Fails with mysterious charmap error, doesn't work on my machine so disabled. UPDATE: its probably some shit coding
#printf "upgrading pip... "
#wine py -m pip -q install --upgrade pip
#echo "done"
#
## bad idea
##printf "winetricks: installing windowscodecs... "
##winetricks windowscodecs #> /dev/null
##echo "done"
#
#printf "installing dependencies... "
#wine py -m pip -q install --no-warn-script-location -r requirements.txt # > /dev/null
#echo "done"
#
#printf "building exe... "
#sleep 5
#echo ""
## this is so bad lmao
#wine "c:\\users\\$USER\\appdata\\local\\programs\\python\\python38\\Scripts\\pyinstaller" \
#    --distpath ./build/dist --noconfirm --log-level DEBUG unnamed-launcher.spec
#echo "done"
#
#printf "removing things... "
#rm requirements.txt
#echo "done"
