# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import os
import stat
import threading
import urllib.request
import urllib.error

from gi.repository import GLib

PAWNS_CLI_URL = (
    'https://pawns-app.s3.eu-central-1.amazonaws.com'
    '/cli/latest/linux_x86_64/pawns-cli'
)


class PawnsCLIDownloader:
    """Downloads the Pawns CLI binary to the user's data directory."""

    def __init__(self):
        self._data_dir = os.path.join(
            GLib.get_user_data_dir(), 'chessboard'
        )
        os.makedirs(self._data_dir, exist_ok=True)

    @property
    def cli_path(self):
        return os.path.join(self._data_dir, 'pawns-cli')

    def download_async(self, callback):
        """Download the CLI binary in a background thread.

        Args:
            callback: A callable(success: bool, error_msg: str | None)
                      invoked when the download finishes.
        """
        thread = threading.Thread(
            target=self._download_thread,
            args=(callback,),
            daemon=True,
        )
        thread.start()

    def _download_thread(self, callback):
        try:
            dest = self.cli_path
            urllib.request.urlretrieve(PAWNS_CLI_URL, dest)
            # Make executable
            st = os.stat(dest)
            os.chmod(dest, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
            callback(True, None)
        except urllib.error.URLError as exc:
            callback(False, str(exc.reason))
        except OSError as exc:
            callback(False, str(exc))
        except Exception as exc:
            callback(False, str(exc))
