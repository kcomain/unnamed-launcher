from logging import getLogger
from typing import Callable, Union

from PySide6.QtWidgets import QApplication, QDialog, QWidget

from .helpers import load_ui


class BaseEvents:
    """Base class that event handlers should subclass"""

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
            logger.debug("no event listeners found...?")

        for i in listeners:
            try:
                logger.debug(f"attempting to register event handler {i.__name__}")
                i(self.logger.getChild(i.__name__.replace("event_", "")))
            except Exception as e:
                logger.debug(f"failure at registering event handler {i.__name__}: {e}")
            else:
                logger.debug(f"registered event handler {i.__name__} successfully")


class MenuEvents(BaseEvents):
    def __init__(self, app: QApplication, window):
        super().__init__(app, window)

    def event_menu_quit(self, logger):
        def action():
            logger.debug("quit action called")
            self.app.quit()

        self.window.menu_quit.triggered.connect(action)

    def event_menu_about(self, logger):
        def action():
            logger.debug("about window action called")
            logger.debug("attempting to load about dialog")
            about_ui: Union[QDialog, QWidget] = load_ui("AboutDialog")

            about_ui.exec()

        self.window.menu_about.triggered.connect(action)


def init(app: QApplication, window):
    MenuEvents(app, window).init()
