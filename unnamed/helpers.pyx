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
import os

from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget

from . import VERSION


cdef bint DEV_BUILD
try:
    from . import __release__
except ImportError:
    DEV_BUILD = True
else:
    DEV_BUILD = False

cdef object logger
logger = logging.getLogger("helpers")


cpdef object load_ui(name: str):
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


cpdef str get_version():
    base = f"v{VERSION.numerical_string} {VERSION.release}"
    if DEV_BUILD:
        return str(f'{base} {"git+" + VERSION.revision if VERSION.rev != "" else ""} (dev build)')
    else:
        return str(base)
