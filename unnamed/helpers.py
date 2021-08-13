import logging
import os
from typing import Union

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

logger = logging.getLogger("helpers")


def load_ui(name: str) -> QWidget:
    loader = QUiLoader()
    _logger = logger.getChild("load_ui")

    _logger.debug(f"attempting to load ui file `{name}.ui`")
    basedir = os.path.dirname(os.path.realpath(__file__))
    ui_path = os.path.join(basedir, f"ui/{name}.ui")
    ui_file = QFile(ui_path)

    if not ui_file.open(QFile.ReadOnly):
        _logger.warning(f"unable to load ui file: {ui_file.errorString()}")
        _logger.debug(f"current location: {basedir}")
        _logger.debug(f"ui file path: {ui_path}")
        raise OSError(f"unable to load ui file `{name}`: {ui_file.errorString()}")

    ui = loader.load(ui_file)
    _logger.debug(f"loaded ui file `{name}.ui` successfully")
    return ui
