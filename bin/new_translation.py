"""
Embodiment of laziness

"""

#  Copyright (c) 2021 kcomain and contributors
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

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
