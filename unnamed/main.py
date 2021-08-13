import os
import sys

from PySide6.QtCore import QFile  # , QTranslator
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from unnamed.events import init as events_init

try:
    from unnamed.resources import qInitResources
except ImportError:
    print(
        "unable to import resources file. is the file generated? (try running make compile-resource)"
    )
    sys.exit(1)


def main():
    # i have no idea what this is used apart from running the actual thing
    app = QApplication(sys.argv)
    qInitResources()
    print("initialized resources")

    # load translations (should be done when user changes language or if set language is not en_US,
    # not on startup - i think)

    # translator = QTranslator()
    # if translator.load(":/data/resources/translations.qm"):
    #     print("loaded translations")
    #     app.installTranslator(translator)
    # else:
    #     print(f"unable to load translations. is the resource file compiled or is the qm file empty?")

    # load the main window
    loader = QUiLoader()

    basedir = os.path.dirname(os.path.realpath(__file__))
    main_window_f = QFile(os.path.join(basedir, "ui/MainMenu.ui"))
    if not main_window_f.open(QFile.ReadOnly):
        print(f"unable to load mainwindow ui: {main_window_f.errorString()}")
        print(f"current location: {os.getcwd()}")
        sys.exit(1)
    main_window = loader.load(main_window_f)

    # load events
    events_init(app, main_window)

    main_window.show()
    app.exec()


if __name__ == "__main__":
    main()
