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

from PySide6.QtCore import QThread, Signal

from .thcrap import Repository


class ThWorker(QThread):
    """"""

    progress = Signal(int, int)
    failure = Signal(str)
    finish = Signal(bool)

    failed = False

    def __init__(self, repo: Repository, parent=None, logger=None):
        super().__init__(parent)
        thing = type("Logger", (), {"debug": lambda _: None})
        self.repo = repo
        self.logger = logger if logger else thing

    def run(self):
        self.logger.debug("syncing repository")
        self.repo.sync(2, signal=self.progress, fail_signal=self.failure)
        self.finish.emit(False)

        self.sleep(5)
        self.finish.emit(True)


def update_text(window):
    def i_think_this_might_work(current, total):
        window.funny.setMaximum(total)
        window.funny.setValue(current)
        window.thcrap_test.setText(f"Updating repos... [{current}/{total}]")
        return

    return i_think_this_might_work


def update_failure(window):
    def staspriaj(message):
        window.test_thread.failed = True
        window.funny.setFormat(f"error: {message}")
        window.funny.setMaximum(100)
        return

    return staspriaj


def finish_update(window):
    def probably_works_question_mark(button_enable):
        if button_enable:
            window.thcrap_test.setEnabled(True)
            window.thcrap_test.setText("Test thcrap (debug only)")
        else:
            window.thcrap_test.setText("Finished updating.")

        if window.test_thread.failed:
            return
        return

    return probably_works_question_mark


def test(window, logger):
    window.funny.setFormat("%p%")
    repo = window.thcrap_starting_text.text()
    logger.debug(f"text of starting repo is {repo}")
    repo_ = Repository(repo)
    thread = ThWorker(repo_, logger=logger)
    thread.progress.connect(update_text(window))
    thread.finish.connect(finish_update(window))
    thread.failure.connect(update_failure(window))
    thread.start()
    logger.debug("started worker thread")
    return thread
