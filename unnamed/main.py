import logging
import sys

from PySide6.QtWidgets import QApplication

from unnamed.events import init as events_init
from unnamed.helpers import load_ui

try:
    from unnamed.resources import qInitResources
except ImportError:
    logging.critical("unable to import resources file. is the file generated? (try running make compile-resource)")
    sys.exit(1)


def app():
    # setup logging
    logger = logging.getLogger("app")

    # i have no idea what this is used apart from running the actual thing
    app = QApplication(sys.argv)
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
    try:
        main_window = load_ui("MainMenu")
    except OSError:
        logger.critical(
            "can't load main window ui file. this program is a brick.' "
            "please report to the dev (with debug logs pls, set environment variable LOGGING to debug)"
        )
        sys.exit(1)

    # load events
    events_init(app, main_window)

    main_window.show()
    app.exec()


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
