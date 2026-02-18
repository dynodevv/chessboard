import subprocess
import signal

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import GLib


class ProcessManager:
    def __init__(self, on_died_callback=None):
        self._process = None
        self._monitor_id = None
        self._on_died = on_died_callback

    def start(self, email, password):
        if self.is_running():
            return

        cmd = [
            "./pawns-cli",
            f"-email={email}",
            f"-password={password}",
            "-device-name=Chessboard-Linux",
            "-accept-tos",
        ]

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            if self._on_died:
                self._on_died()
            return

        self._monitor_id = GLib.timeout_add_seconds(5, self._check_process)

    def stop(self):
        if self._monitor_id is not None:
            GLib.source_remove(self._monitor_id)
            self._monitor_id = None

        if self._process and self._process.poll() is None:
            self._process.send_signal(signal.SIGTERM)
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()

        self._process = None

    def is_running(self):
        return self._process is not None and self._process.poll() is None

    def _check_process(self):
        if self._process and self._process.poll() is not None:
            self._process = None
            self._monitor_id = None
            if self._on_died:
                self._on_died()
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE
