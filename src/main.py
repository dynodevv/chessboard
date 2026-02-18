import sys

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

from window import ChessboardWindow


class ChessboardApplication(Adw.Application):
    def __init__(self, version):
        super().__init__(
            application_id='org.dynodevv.chessboard',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )
        self._version = version
        self._setup_actions()

    def _setup_actions(self):
        about_action = Gio.SimpleAction.new('about', None)
        about_action.connect('activate', self._on_about)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', self._on_quit)
        self.add_action(quit_action)
        self.set_accels_for_action('app.quit', ['<Control>q'])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ChessboardWindow(application=self)
        win.present()

    def _on_about(self, action, param):
        about = Adw.AboutDialog(
            application_name='Chessboard',
            developer_name='Dyno',
            version=self._version,
            website='https://github.com/dynodevv/chessboard',
            issue_url='https://github.com/dynodevv/chessboard/issues',
            comments='A premium Linux client for Pawns.app CLI.\n\n'
                     'This project is not associated, nor endorsed by IPRoyal.',
            license_type=Gtk.License.MIT_X11,
            developers=['Dyno'],
        )
        about.present(self.props.active_window)

    def _on_quit(self, action, param):
        self.quit()


def main(version):
    app = ChessboardApplication(version)
    return app.run(sys.argv)
