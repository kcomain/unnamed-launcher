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
from PySide6.QtCore import QRegularExpression as QRe
from PySide6.QtGui import QRegularExpressionValidator as QReValidator
from PySide6.QtWidgets import QFileDialog

from . import BaseEvents


class SettingInputEvents(BaseEvents):
    def event_np2_browse_click(self, logger):
        def action():
            logger.debug("browse np2 location button clicked")
            logger.debug("attempting to show file dialog...")
            file, _ = QFileDialog.getOpenFileName(self.window, filter="Executable files (*.exe)")
            logger.debug(f"selected file: {file}")
            if file == "":
                logger.debug("file returned is empty, not setting line")
            else:
                logger.debug(f"setting text of LineEdit to {file}")
                self.window.np2_location_text.setText(file)
            logger.debug("WIP: saving location")

        self.window.np2_location_browse.clicked.connect(action)

    def event_thcrap_browse_click(self, logger):
        def action():
            logger.debug("browse thcrap location button clicked")
            logger.debug("attempting to show file dialog...")
            file, _ = QFileDialog.getOpenFileName(self.window)
            logger.debug(f"selected file: {file}")
            if file == "":
                logger.debug("file returned is empty, not setting line")
            else:
                logger.debug(f"setting text of LineEdit to {file}")
                self.window.thcrap_text.setText(file)
            logger.debug("WIP: saving location")

        self.window.thcrap_browse.clicked.connect(action)

    # def event_
