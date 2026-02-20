# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gio, GLib, Gtk

from chessboard.window import ChessboardWindow
from chessboard.preferences import ChessboardPreferencesDialog


class ChessboardApplication(Adw.Application):

    def __init__(self, version='1.0.0', **kwargs):
        super().__init__(
            application_id='org.dynodevv.chessboard',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            **kwargs,
        )
        self._version = version
        self._setup_actions()

    def _setup_actions(self):
        actions = [
            ('quit', self._on_quit, ['<primary>q']),
            ('about', self._on_about, None),
            ('preferences', self._on_preferences, ['<primary>comma']),
        ]
        for name, callback, accels in actions:
            action = Gio.SimpleAction.new(name, None)
            action.connect('activate', callback)
            self.add_action(action)
            if accels:
                self.set_accels_for_action(f'app.{name}', accels)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ChessboardWindow(application=self)
        win.present()

    def _on_quit(self, _action, _param):
        win = self.props.active_window
        if win:
            win.on_close()
        self.quit()

    def _on_about(self, _action, _param):
        about = Adw.AboutDialog(
            application_name='Chessboard',
            application_icon='org.dynodevv.chessboard',
            developer_name='Dyno',
            version=self._version,
            developers=['Dyno'],
            copyright='© 2026 Dyno',
            license_type=Gtk.License.MIT_X11,
            website='https://github.com/dynodevv/chessboard',
            issue_url='https://github.com/dynodevv/chessboard/issues',
            comments=(
                'A premium Linux client for Pawns CLI.\n\n'
                'This project is not associated, nor endorsed by IPRoyal.'
            ),
        )
        about.present(self.props.active_window)

    def _on_preferences(self, _action, _param):
        prefs = ChessboardPreferencesDialog()
        prefs.present(self.props.active_window)
