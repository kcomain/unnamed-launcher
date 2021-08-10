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

build-executable: dependencies compile-resource
	pyinstaller \
		--distpath ./build/dist \
		--log-level DEBUG \
		--name unnamed-launcher \
		--icon unnamed/resources/reimu.ico \
		--noconsole \
		--onedir \
		--noupx \
		--noconfirm \
		--collect-all unnamed \
		main.py

clean:
	rm -vfr build unnamed/resources.py *.spec