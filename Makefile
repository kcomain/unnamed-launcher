PWD = $(shell pwd)
export MAKE_ENV = true

all: dependencies compile-resource lint

dependencies:
	poetry install

lint:
	isort unnamed
	black unnamed bin --line-length=120

compile-resource:
	pyside6-rcc unnamed/resources.qrc -o unnamed/resources.py
	lupdate unnamed -ts unnamed/resources/translation.*.ts || true

release-qm:
	lrelease unnamed/resources/translation.*.ts

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

clean:
	rm -vfr build unnamed/resources.py temp dist requirements.txt || true
