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

start: compile-resource build
	LOGGING=debug python3 main.py

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

.PHONY: build
build:
	python setup.py build_ext --inplace

clean:
	rm -vfr build unnamed/resources.py temp dist requirements.txt || true
	find -name '*.c' -print -delete  # this is a python repo,
	find -name '*.so' -print -delete
