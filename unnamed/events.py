from logging import getLogger
from typing import Callable, Union

from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QWidget

from .helpers import load_ui
from .th_crap import test


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


class ThCrapTest(BaseEvents):
    def event_thcrap_test(self, logger):
        def action():
            self.window.thcrap_test.setEnabled(False)
            self.window.test_thread = test(self.window, logger)

        self.window.thcrap_test.clicked.connect(action)


def init(app: QApplication, window):
    MenuEvents(app, window).init()
    SettingInputEvents(app, window).init()
    ThCrapTest(app, window).init()
