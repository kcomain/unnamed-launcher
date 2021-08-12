@REM build-windows.bat
@REM Version 1.0
@REM I do not know how well this works, I guess we will see.

@echo off

echo Hello, this script will build this project with pyinstaller
echo The built program can be found in build/dist/ if all goes well
echo.

REM i actually want to find a way to automatically detect this, but my last remaining brain cell protested so that's not happening.
echo your current directory is %cd%
echo please make sure you're in the root directory (i.e. unnamed-launcher instead of unnamed-launcher\bin) before continuing
echo.
echo if you're running this script directly from explorer, please don't. instead, open up a cmd window, type cd and then
echo **DRAG** the unnamed-launcher folder to the cmd window, then press return. after that, type bin\build-windows.bat
echo and press enter. you will see this message again.
pause

echo.

echo First, we need to check some stuff.
<NUL set /p nl=Checking for python...
which python 2>NUL
if ERRORLEVEL 1 (
    echo cannot find python
    echo python is not in PATH, and I don't know where python is. please add python to PATH first
    pause
    exit 1
)

<NUL set /p nl=Checking for poetry...
which poetry 2>NUL
if ERRORLEVEL 1 (
    echo poetry doesn't exist, that's fine.
    set /a POETRYFOUND=0
) else (
    goto poetryfound
)

<NUL set /p nl=Checking for pip...
python -m pip -V
if ERRORLEVEL 1 (
    echo pip doesn't exist, what the hell is this system
    echo attempting installation anyways.
    goto pipfound
) else (
    echo pip found
    goto pipfound
)
REM in hindsight i could've probably used %LOCALAPPDATA% but i cannot be bothered. windows sucks.

echo You should not be here.

REM ====================================================================================================================
:poetryfound
echo executing poetry specific instructions

echo installing dependencies
poetry install

echo generating required items
poetry run pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py

echo building executable
poetry run pyinstaller ^
    --distpath .\build\dist ^
    --log-level WARN ^
	--noconfirm ^
	--onefile ^
	--name unnamed-launcher ^
	--noconsole ^
	--noupx ^
	--icon unnamed/resources/reimu.ico ^
	--collect-data unnamed ^
	--collect-binaries unnamed ^
	main.py

if ERRORLEVEL neq 0 (
    echo building failed for some reason.
    exit 1
)

goto done

REM ====================================================================================================================
:pipfound
echo executing pip-specific instructions

echo creating a virtual environment
python -m venv venv --upgrade-deps 2>nul
if ERRORLEVEL neq 0 (
    REM 3.9 lower?
    python -m venv venv
    venv\scripts\pip install -U pip 2>nul
)
venv\scripts\pip install -U wheel

echo installing dependencies
venv\scripts\pip install -r requirements.txt

echo generating required files
venv\scripts\pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py
REM technically regenerating/"publishing" the translations file would be great but there's no
REM way to make the user install the large ass qt dep just to run/build this

echo building executable
venv\scripts\pyinstaller ^
    --distpath .\build\dist ^
    --log-level WARN ^
	--noconfirm ^
	--onefile ^
	--name unnamed-launcher ^
	--noconsole ^
	--noupx ^
	--icon unnamed/resources/reimu.ico ^
	--collect-data unnamed ^
	--collect-binaries unnamed ^
	main.py

goto done

REM ====================================================================================================================
:done
echo script finished.
pause
