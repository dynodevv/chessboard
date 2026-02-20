# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import sys

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gio

from chessboard.application import ChessboardApplication


def main(version):
    app = ChessboardApplication(version=version)
    return app.run(sys.argv)
