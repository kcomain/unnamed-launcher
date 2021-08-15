[![Build executables](https://github.com/kcomain/unnamed-launcher/actions/workflows/build-executable.yml/badge.svg)](https://github.com/kcomain/unnamed-launcher/actions/workflows/build-executable.yml)
[![wakatime](https://wakatime.com/badge/github/kcomain/unnamed-launcher.svg)](https://wakatime.com/badge/github/kcomain/unnamed-launcher)
<hr>

# unnamed-launcher

note: this is a crappy ass project that no one should use

yet another 2hu launcher

design basically stolen from [widdiful's launcher](https://www.widdiful.co.uk/touhou.html) 
and [this version](https://github.com/David-JonesDVN/Touhou-Relauncher)

_might_ work on windows, _should_ work on linux, probably will never work on macos past catalina 

## how to run?
because this is written in (sorry) python, you just need to
1. clone the repo
```bash
git clone https://github.com/kcomain/unnamed-launcher
# or
git clone git@github.com:kcomain/unnamed-launcher
```
2. install all the required stuff
```bash
poetry install
# or
# you might want to get into a virtual env first:
python -m venv venv
source venv/bin/activate # linux
.\venv\bin\activate.bat # windows

pip install -r requirements.txt
```
3. and then do
```bash
python3 -m unnamed
```

alternatively you can grab executables [here](https://github.com/kcomain/unnamed-launcher/releases/latest)

## runtime requirements
an operating system with 64 bit support

## build requirements
_**Tip:** you only need to do these if you want to build an executable, which you probably don't need to._
_Check out [this](https://github.com/kcomain/unnamed-launcher/releases)_
- Python >=3.6, <3.10

### how to build?
- Linux users
```bash
# if you have gnu make
make all build-executable
```

```bash
# if you don't have gnu make
# 1. install dependencies as shown in #how-to-run
# 2. run the following
pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py
pyinstaller --distpath ./build/dist --log-level WARN --noconfirm --onefile \
    --name unnamed-launcher --noconsole --noupx --collect-data unnamed main.py
```

- Windows users
```bat
bin\build-windows.bat
```

# credits
this project is possible with efforts from the following people:
- [Widdiful](https://www.widdiful.co.uk) for the original launcher
- [David-JonesDVN](https://github.com/David-JonesDVN) for the updated launcher 
- [u/absolitud3](https://old.reddit.com/r/touhou/comments/3jxj3g/im_making_more_sprites/) for the icon
- [zun/team shanghai alice](https://www16.big.or.jp/~zun/) for the amazing games
- [qt/pyside](https://www.qt.io)

disclaimer: this project is not endorsed or supported by the aforementioned entities, team shanghai alice and twilight
frontier. 
i own only the code for this app, if you're the author of any assets that i've used, and you don't want me to use it, 
please [let me know](mailto:me@kcomain.dev)

## todo
- [hard] cut down the binary size
  - how in miku's name does the linux pyinstaller'd binary get to 250 mb i do not understand
- button box wrapping thing (reimplement flowlayout)
- linux compatibility (wine, steam proton, etc.)
