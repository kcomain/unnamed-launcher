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
from PySide6.QtCore import QDir
from PySide6.QtCore import QRegularExpression as QRe
from PySide6.QtGui import QRegularExpressionValidator as QReV
from PySide6.QtWidgets import QCompleter, QFileSystemModel

from ..helpers import get_version
from . import BaseEvents

URL_RE = QRe(r"^https?://.+\..{1,63}(/.*)*$")
URL_REV = QReV(URL_RE)
FS_MODEL = QFileSystemModel()
FS_MODEL.setRootPath(QDir.currentPath())


class InitEvents(BaseEvents):
    def populate_labels(self):
        self.window.info_version.setText(get_version())

    def set_validators(self):
        self.window.thcrap_starting_text.setValidator(URL_REV)
        self.logger.debug("validators set")

    def set_completer(self):
        np2_completer = QCompleter(FS_MODEL)
        thc_completer = QCompleter(FS_MODEL)
        np2_completer.setCompletionMode(QCompleter.PopupCompletion)
        thc_completer.setCompletionMode(QCompleter.PopupCompletion)
        self.window.np2_location_text.setCompleter(np2_completer)
        self.window.thcrap_text.setCompleter(thc_completer)
        self.logger.debug("completers set")

    def run_all(self):
        self.populate_labels()
        self.set_validators()
        self.set_completer()
