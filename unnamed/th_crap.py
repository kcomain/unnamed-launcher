from .thcrap import Repository


def test(window, logger):
    repo = window.thcrap_starting_text.text()
    logger.debug(f"text of starting repo is {repo}")
    repo = Repository(repo)
    repo.sync(2)
    return
