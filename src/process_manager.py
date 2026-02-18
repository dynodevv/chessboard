import os
import shutil
import subprocess
import signal

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import GLib

PAWNS_CLI_DEFAULT = "./pawns-cli"


class ProcessManager:
    def __init__(self, on_died_callback=None):
        self._process = None
        self._monitor_id = None
        self._on_died = on_died_callback
        self._log_fh = None

    @staticmethod
    def _find_pawns_cli():
        env_path = os.environ.get("PAWNS_CLI_PATH")
        if env_path and os.path.isfile(env_path):
            return env_path
        found = shutil.which("pawns-cli")
        if found:
            return found
        return PAWNS_CLI_DEFAULT

    def start(self, email, password, log_file=None):
        if self.is_running():
            return True

        cli = self._find_pawns_cli()
        cmd = [
            cli,
            f"-email={email}",
            f"-password={password}",
            "-device-name=Chessboard-Linux",
            "-accept-tos",
        ]

        stdout_target = subprocess.DEVNULL
        stderr_target = subprocess.DEVNULL
        if log_file:
            try:
                self._log_fh = open(log_file, "w", encoding="utf-8")
                stdout_target = self._log_fh
                stderr_target = self._log_fh
            except OSError:
                pass

        try:
            self._process = subprocess.Popen(
                cmd,
                stdout=stdout_target,
                stderr=stderr_target,
            )
        except FileNotFoundError:
            self._close_log()
            return False

        self._monitor_id = GLib.timeout_add_seconds(5, self._check_process)
        return True

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
        self._close_log()

    def is_running(self):
        return self._process is not None and self._process.poll() is None

    def _close_log(self):
        if self._log_fh:
            try:
                self._log_fh.close()
            except OSError:
                pass
            self._log_fh = None

    def _check_process(self):
        if self._process and self._process.poll() is not None:
            self._process = None
            self._monitor_id = None
            self._close_log()
            if self._on_died:
                self._on_died()
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE
