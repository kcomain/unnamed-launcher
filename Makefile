PWD = $(shell pwd)

all: dependencies compile-resource lint

dependencies:
	poetry install

lint:
	isort unnamed
	black unnamed --line-length=120

compile-resource:
	pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py
	lupdate unnamed -ts unnamed/resources/translations.ts || true

generate-requirements:
	poetry export --dev --without-hashes -f requirements.txt > requirements.txt

start:
	LOGGING=debug python3 -m unnamed

build-executable: all
	pyinstaller  \
		--distpath ./build/dist \
		--log-level WARN \
		--noconfirm \
		--onefile \
		--name unnamed-launcher \
		--noconsole \
		--noupx \
		--collect-data unnamed \
		main.py

		@#--collect-binaries unnamed
		@#--icon unnamed/resources/reimu.ico
		@#--onedir
		@#unnamed-launcher.spec

	@#bash bin/build-windows.sh
#	curl https://github.com/kcomain/docker-pyinstaller/raw/master/Dockerfile-py3-win64 -Lo temp/Dockerfile
#	cd temp && docker build -t pyinstaller-windows .
#	docker run -v "$(PWD):/src/" pyinstaller-windows

clean:
	rm -vfr build unnamed/resources.py temp dist requirements.txt || true
