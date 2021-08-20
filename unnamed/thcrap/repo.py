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
import urllib.parse
from json import JSONDecodeError
from typing import Union

import requests

from unnamed.thcrap import _logger

# from appdirs import user_cache_dir


class Repository:
    """
    Object representation of a thcrap repository
    """

    __slots__ = (
        # public
        "url",
        "neighbors",
        "repo_id",
        "contact",
        "title",
        "patches",
        #
        # private
        "_synced",
        "_logger",
        "_total",
    )

    def __init__(self, url):  # , repo_id=None):
        self.url = url
        self.neighbors = {None: []}
        self.repo_id = None  # repo_id
        self.patches = {}
        self.contact = "unnamed@kcomain.dev"
        self.title = "Unknown repository"

        self._synced = []  # prevent recursive loops
        self._total = 0
        self._logger = _logger.getChild("unnamed_repository")

    def __str__(self):
        return f""

    def sync(
        self,
        neighbor_sync_depth: int = 0,
        cache: bool = True,
        signal=None,
        fail_signal=None,
        _self=None,
        _iter=0,
    ) -> int:
        """
        Sync repository

        :param _self: private
        :param _iter: private
        :param signal: pyqt/pyside signal emitted on progress update
        :param fail_signal: pyqt/pyside signal emitted on failure
        :param neighbor_sync_depth: How deep to sync neighbors, 0 to disable, defaults to 0
        :param cache: Whether or not to cache results, defaults to yes
        :return: private
        """
        if not signal:
            signal = type("DummySignal", (), {"emit": lambda _: None})
        if not fail_signal:
            fail_signal = type("DummySignal", (), {"emit": lambda _: None})

        if not _self:
            _self = self

        signal.emit(_iter, _self._total)
        self._logger.debug(
            f"syncing repository {self.url}",
        )
        # future code for loading from cache goes here, idea is load from cache then return immediately
        _ = cache
        # future code end
        _self._synced.append(self.url.strip("/"))
        repo = self._hit(_iter, signal, fail_signal)
        if repo is None:
            self._logger.debug("invalid repository? please report")
            return _iter
        self.repo_id = repo["id"]
        self.patches = repo["patches"]  # required attribute

        self.title = repo.get("title", self.repo_id)
        self.contact = repo.get("contact", None)

        self._logger = logging.getLogger(self.repo_id)

        if "neighbors" not in repo:
            self._logger.debug(f"there are no neighbors for {self.repo_id}")
            return _iter

        # embodiment of pain and suffering
        self._logger.debug(f'there are {len(repo["neighbors"])} neighbor(s) for {self.url}')
        neighbors = []
        for neighbor in repo["neighbors"]:
            if neighbor_sync_depth == 0:
                continue
            neighbor = neighbor.strip("/")
            if neighbor in _self._synced:
                self._logger.debug(f"neighbor {neighbor} already added, not adding again")
                continue
            neighbors.append(neighbor)
            _self._total += 1

        for neighbor in neighbors:
            _self._synced.append(neighbor)

            n_repo = Repository(neighbor)
            if neighbor_sync_depth != 0:
                _iter = n_repo.sync(neighbor_sync_depth - 1, signal=signal, _iter=_iter + 1, _self=_self)
            else:
                self._logger.debug("neighbor sync depth reached 0, not syncing")

            if n_repo.repo_id is None:
                self.neighbors[n_repo.repo_id].append(n_repo)
            else:
                self.neighbors[n_repo.repo_id] = n_repo  # noqa
        return _iter

    def _hit(self, iter_c, sig, sigerr) -> Union[dict, None]:
        _ = sig  # might come in handy later
        logger = self._logger.getChild("http")
        path = urllib.parse.urljoin(self.url + "/", "repo.js")
        logger.debug(self.url)
        try:
            res = requests.get(path)
        except requests.ConnectionError as e:
            sigerr.emit(f"Connection error: {e}")
            return None
        try:
            res.raise_for_status()
        except requests.HTTPError:
            # why python why (waiting for 3.10 release)
            if res.status_code == 404:
                logger.info(f"[NotFound:{iter_c}] {path}")
            else:
                logger.info(f"[UnknownStatus({res.status_code}:{iter_c}] {path}")
            return None

        try:
            j = res.json()
            logger.info(f"[Hit:{iter_c}] {path}")
            return j
        except JSONDecodeError:
            logger.info(f"[InvalidJSON:{iter_c}] {path}")
            return None
