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
import logging
from typing import Union

from PySide6.QtWidgets import QDialog, QWidget

from ..helpers import load_ui
from . import BaseEvents


class MenuEvents(BaseEvents):
    def event_menu_quit(self, logger: logging.Logger):
        def action():
            logger.debug("quit action called")
            self.app.quit()

        self.window.menu_quit.triggered.connect(action)

    def event_menu_about(self, logger: logging.Logger):
        def action():
            logger.debug("about window action called")
            logger.debug("attempting to load about dialog")
            about_ui: Union[QDialog, QWidget] = load_ui("AboutDialog")

            about_ui.exec()

        self.window.menu_about.triggered.connect(action)
