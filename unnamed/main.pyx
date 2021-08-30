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
import sys

from PySide6.QtWidgets import QApplication

from unnamed.events import init as events_init
from unnamed.events.init import InitEvents
from unnamed.helpers import load_ui

try:
    from unnamed.resources import qInitResources
except ImportError:
    logging.critical("unable to import resources file. is the file generated? (try running make compile-resource)")
    sys.exit(1)


# noinspection SpellCheckingInspection
cdef app():
    # setup logging
    cdef object logger = logging.getLogger("app")

    # i have no idea what this is used apart from running the actual thing
    cdef object qapp = QApplication(sys.argv)
    qInitResources()
    logger.debug("initialized resources")

    # load translations (should be done when user changes language or if set language is not en_US,
    # not on startup - i think)

    # translator = QTranslator()
    # if translator.load(":/data/resources/translations.qm"):
    #     print("loaded translations")
    #     app.installTranslator(translator)
    # else:
    #     print(f"unable to load translations. is the resource file compiled or is the qm file empty?")

    # load the main window
    cdef object main_window
    try:
        main_window = load_ui("MainMenu")
    except OSError:
        logger.critical(
            "can't load main window ui file. this program is a brick.' "
            "please report to the dev (with debug logs pls, set environment variable LOGGING to debug)"
        )
        sys.exit(1)

    # load events
    events_init(qapp, main_window)
    cdef object init_ev = InitEvents(qapp, main_window)
    init_ev.run_all()

    main_window.show()
    qapp.exec()


def main():
    try:
        app()
    except Exception:
        logging.critical("If you're seeing this message, this means the application died for some reason.")
        logging.critical("There should be a stacktrace below this message that describes what went wrong.")
        logging.critical("If you can't see that message, you might have set the log level to critical or higher.")
        logging.critical("Consider lowering it to learn why.")
        logging.exception("app() thrown an exception")
        logging.critical("unable to continue as app is in unknown state, exiting")
        sys.exit(1)


if __name__ == "__main__":
    main()
