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

from logging import getLogger
from typing import Callable

from PySide6.QtWidgets import QApplication


class BaseEvents:
    """Base class that event handlers should subclass

    To load an event handler, name a method with ``event_`` as prefix

    example: ``event_version_ui_open``

    do NOT return anything as they will not be processed in any way.
    """

    def __init__(self, app: QApplication, window):
        self.app = app
        self.window = window
        self.logger = getLogger(self.__class__.__name__)

    def init(self):
        # find all functions starting with 'event_'
        logger = self.logger.getChild("init")
        listeners: list[Callable] = []
        for i in dir(self):
            if i.startswith("event_"):
                logger.debug(f"found function {i}")
                listeners.append(getattr(self, i))

        if len(listeners) == 0:
            logger.debug("no event listeners found")

        for i in listeners:
            try:
                logger.debug(f"attempting to register event handler {i.__name__}")
                i(self.logger.getChild(i.__name__.replace("event_", "")))
            except Exception as e:
                logger.debug(f"failure at registering event handler {i.__name__}: {e}")
            else:
                logger.debug(f"registered event handler {i.__name__} successfully")
