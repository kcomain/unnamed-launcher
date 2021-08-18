from PySide6.QtCore import QThread, Signal

from .thcrap import Repository


class ThWorker(QThread):
    """"""

    progress = Signal(int, int)
    finish = Signal()

    def __init__(self, repo: Repository, parent=None, logger=None):
        super().__init__(parent)
        thing = type("Logger", (), {"debug": lambda _: None})
        self.repo = repo
        self.logger = logger if logger else thing

    def run(self):
        self.logger.debug("syncing repository")
        self.repo.sync(2, signal=self.progress)
        self.finish.emit()


def update_text(window):
    def i_think_this_might_work(current, total):
        window.funny.setMaximum(total)
        window.funny.setValue(current)
        window.funny.setFormat(f"Updating repos... [{current}/{total}] %p%")
        return

    return i_think_this_might_work


def finish_update(window):
    def probably_works_question_mark():
        window.funny.setFormat("Finished updating.")
        return

    return probably_works_question_mark


def test(window, logger):
    repo = window.thcrap_starting_text.text()
    logger.debug(f"text of starting repo is {repo}")
    repo_ = Repository(repo)
    thread = ThWorker(repo_, logger=logger)
    thread.progress.connect(update_text(window))
    thread.finish.connect(finish_update(window))
    thread.start()
    logger.debug("started worker thread")
    return thread
