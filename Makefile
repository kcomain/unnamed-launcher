PWD = $(shell pwd)

all: dependencies compile-resource lint

dependencies:
	poetry install

lint:
	isort .
	black .

compile-resource:
	pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py
	lupdate unnamed -ts unnamed/resources/translations.ts

start:
	python3 -m unnamed

build-executable: all
	pyinstaller  \
		--distpath ./build/dist \
		--log-level DEBUG \
		--noconfirm \
		--onefile \
		--name unnamed-launcher \
		--icon unnamed/resources/reimu.ico \
		--noconsole \
		--noupx \
		--collect-all unnamed \
		main.py

		@#--onedir
		@#unnamed-launcher.spec

	bash bin/build-windows.sh
#	curl https://github.com/kcomain/docker-pyinstaller/raw/master/Dockerfile-py3-win64 -Lo temp/Dockerfile
#	cd temp && docker build -t pyinstaller-windows .
#	docker run -v "$(PWD):/src/" pyinstaller-windows

clean:
	rm -vfr build unnamed/resources.py temp dist requirements.txt || true
