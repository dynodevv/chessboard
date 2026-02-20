# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import os

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gio, GLib, Gtk


class ChessboardPreferencesDialog(Adw.PreferencesDialog):

    def __init__(self, **kwargs):
        super().__init__(title='Preferences', **kwargs)

        self._settings = Gio.Settings.new('org.dynodevv.chessboard')

        page = Adw.PreferencesPage()
        self.add(page)

        # ── Startup group ────────────────────────────────────────────
        startup_group = Adw.PreferencesGroup(
            title='Startup',
            description='Configure automatic startup behaviour.',
        )
        page.add(startup_group)

        # Auto-start sharing when Chessboard opens
        self._autostart_sharing_row = Adw.SwitchRow(
            title='Auto-start Internet Sharing',
            subtitle='Start Pawns CLI automatically when Chessboard launches.',
        )
        self._autostart_sharing_row.set_active(
            self._settings.get_boolean('autostart-sharing')
        )
        self._autostart_sharing_row.connect(
            'notify::active', self._on_autostart_sharing_changed
        )
        startup_group.add(self._autostart_sharing_row)

        # Auto-start Chessboard at login
        self._autostart_app_row = Adw.SwitchRow(
            title='Launch at Startup',
            subtitle='Start Chessboard automatically when you log in.',
        )
        self._autostart_app_row.set_active(
            self._settings.get_boolean('autostart-app')
        )
        self._autostart_app_row.connect(
            'notify::active', self._on_autostart_app_changed
        )
        startup_group.add(self._autostart_app_row)

    # ── Callbacks ────────────────────────────────────────────────────

    def _on_autostart_sharing_changed(self, row, _pspec):
        self._settings.set_boolean('autostart-sharing', row.get_active())

    def _on_autostart_app_changed(self, row, _pspec):
        active = row.get_active()
        self._settings.set_boolean('autostart-app', active)
        self._update_autostart_desktop_file(active)

    def _update_autostart_desktop_file(self, enable):
        """Create or remove the XDG autostart desktop entry."""
        autostart_dir = os.path.join(
            GLib.get_user_config_dir(), 'autostart'
        )
        desktop_path = os.path.join(
            autostart_dir, 'org.dynodevv.chessboard.desktop'
        )

        if enable:
            os.makedirs(autostart_dir, exist_ok=True)
            content = (
                '[Desktop Entry]\n'
                'Type=Application\n'
                'Name=Chessboard\n'
                'Exec=chessboard\n'
                'Icon=org.dynodevv.chessboard\n'
                'Terminal=false\n'
                'X-GNOME-Autostart-enabled=true\n'
            )
            with open(desktop_path, 'w') as f:
                f.write(content)
        else:
            try:
                os.remove(desktop_path)
            except FileNotFoundError:
                pass
