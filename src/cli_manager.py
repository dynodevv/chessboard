# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import os
import signal
import subprocess

from gi.repository import GLib


class PawnsCLIManager:
    """Manages the lifecycle of the Pawns CLI background process."""

    def __init__(self):
        self._process = None
        self._data_dir = os.path.join(
            GLib.get_user_data_dir(), 'chessboard'
        )

    @property
    def cli_path(self):
        return os.path.join(self._data_dir, 'pawns-cli')

    def is_cli_available(self):
        path = self.cli_path
        return os.path.isfile(path) and os.access(path, os.X_OK)

    def is_running(self):
        if self._process is None:
            return False
        return self._process.poll() is None

    def start(self, email, password, device_name):
        """Start the Pawns CLI process in the background.

        Returns True if the process was started successfully.
        """
        if self.is_running():
            return True

        if not self.is_cli_available():
            return False

        cmd = [
            self.cli_path,
            f'-email={email}',
            f'-password={password}',
            f'-device-name={device_name}',
            '-accept-tos',
        ]

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                start_new_session=True,
            )
            return True
        except OSError:
            self._process = None
            return False

    def stop(self):
        """Stop the running Pawns CLI process."""
        if self._process is None:
            return

        if self._process.poll() is None:
            try:
                os.kill(self._process.pid, signal.SIGTERM)
                try:
                    self._process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.kill(self._process.pid, signal.SIGKILL)
                    self._process.wait(timeout=3)
            except OSError:
                pass

        self._process = None
