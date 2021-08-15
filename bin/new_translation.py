"""
Embodiment of laziness

"""

import os
import argparse
import subprocess
import xml.etree.ElementTree as ETree


def shell(command):
    print(f"++++ running {command}")
    return subprocess.run(command, shell=True)


parser = argparse.ArgumentParser(description="Add a new translation file")
parser.add_argument(
    "language",
    help="Locale identifier of the language to add (e.x. en_US, ja_JP, ru_RU) please don't add us locales",
)
args = parser.parse_args()

print(f"+++ language is {args.language}")
shell(f"lupdate unnamed -ts unnamed/resources/translation.{args.language}.ts")
shell("make release-qm")

# lazy
path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../unnamed/resources.qrc")
print("+++ read " + path)
rc = ETree.parse(path)
rc_root = rc.getroot()

print("+++ find all prefix=data attrs")
el = rc_root.find('*/[@prefix="data"]')

print("+++ check for duplicates")
dupe_record = False
for i in el:
    if i.text == f"resources/translation.{args.language}.qm":
        print("!!! dupe entry, not adding")
        dupe_record = True

if not dupe_record:
    file = ETree.SubElement(el, "file")
    file.text = f"resources/translation.{args.language}.qm"
    ETree.indent(rc_root)
    print("=== current xml")
    ETree.dump(rc_root)
    rc.write(path)

shell("make compile-resource")
