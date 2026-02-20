# SPDX-License-Identifier: MIT
# Copyright 2026 Dyno

import os

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gio, GLib, Gtk

from chessboard.download import PawnsCLIDownloader
from chessboard.cli_manager import PawnsCLIManager


class ChessboardWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(
            default_width=500,
            default_height=600,
            title='Chessboard',
            **kwargs,
        )

        self._settings = Gio.Settings.new('org.dynodevv.chessboard')
        self._cli_manager = PawnsCLIManager()
        self._password = ''

        self._build_ui()
        self._check_cli_binary()
        self.connect('close-request', lambda w: self.on_close())

    def on_close(self):
        self._cli_manager.stop()
        return False

    # ── UI Construction ──────────────────────────────────────────────

    def _build_ui(self):
        self._toast_overlay = Adw.ToastOverlay()
        self.set_content(self._toast_overlay)

        self._main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._toast_overlay.set_child(self._main_box)

        # Header bar
        header = Adw.HeaderBar()
        menu_button = Gtk.MenuButton()
        menu_model = Gio.Menu()
        menu_model.append('Preferences', 'app.preferences')
        menu_model.append('About Chessboard', 'app.about')
        menu_button.set_menu_model(menu_model)
        menu_button.set_icon_name('open-menu-symbolic')
        header.pack_end(menu_button)
        self._main_box.append(header)

        # ViewStack for different screens
        self._view_stack = Adw.ViewStack()
        self._main_box.append(self._view_stack)

        self._build_download_page()
        self._build_login_page()
        self._build_dashboard_page()

    def _build_download_page(self):
        page = Adw.StatusPage(
            icon_name='folder-download-symbolic',
            title='Downloading Pawns CLI',
            description='Please wait while the CLI tool is being downloaded…',
        )
        self._download_spinner = Gtk.Spinner(spinning=True)
        self._download_spinner.set_halign(Gtk.Align.CENTER)
        self._download_spinner.set_size_request(32, 32)
        page.set_child(self._download_spinner)

        self._view_stack.add_named(page, 'download')

    def _build_login_page(self):
        page = Adw.StatusPage(
            icon_name='dialog-password-symbolic',
            title='Sign In',
            description=(
                'Enter your IPRoyal Pawns credentials to continue.\n'
                '<b>Important:</b> Two-factor authentication (2FA) must be '
                'disabled in your account due to CLI limitations.'
            ),
        )

        form_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
            halign=Gtk.Align.CENTER,
        )
        form_box.set_size_request(320, -1)

        # Preferences group for login fields
        login_group = Adw.PreferencesGroup()

        self._email_row = Adw.EntryRow(title='Email')
        login_group.add(self._email_row)

        self._password_row = Adw.PasswordEntryRow(title='Password')
        login_group.add(self._password_row)

        self._device_row = Adw.EntryRow(title='Device Name')
        login_group.add(self._device_row)

        form_box.append(login_group)

        # Restore saved settings
        saved_email = self._settings.get_string('email')
        saved_device = self._settings.get_string('device-name')
        if saved_email:
            self._email_row.set_text(saved_email)
        if saved_device:
            self._device_row.set_text(saved_device)
        else:
            self._device_row.set_text(GLib.get_host_name())

        # Login button
        self._login_button = Gtk.Button(label='Sign In')
        self._login_button.add_css_class('suggested-action')
        self._login_button.add_css_class('pill')
        self._login_button.set_halign(Gtk.Align.CENTER)
        self._login_button.set_margin_top(8)
        self._login_button.connect('clicked', self._on_login_clicked)
        form_box.append(self._login_button)

        # Legal disclaimer
        disclaimer = Gtk.Label(
            label='This project is not associated, nor endorsed by IPRoyal.',
            css_classes=['dim-label', 'caption'],
            margin_top=12,
        )
        form_box.append(disclaimer)

        page.set_child(form_box)
        self._view_stack.add_named(page, 'login')

    def _build_dashboard_page(self):
        page_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Clamp for content
        clamp = Adw.Clamp(maximum_size=600)
        clamp.set_margin_top(24)
        clamp.set_margin_bottom(24)
        clamp.set_margin_start(12)
        clamp.set_margin_end(12)

        content = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=24,
        )

        # Status card
        status_group = Adw.PreferencesGroup(title='Internet Sharing')

        self._status_row = Adw.ActionRow(
            title='Status',
            subtitle='Stopped',
        )
        self._status_icon = Gtk.Image.new_from_icon_name('media-playback-stop-symbolic')
        self._status_row.add_prefix(self._status_icon)
        status_group.add(self._status_row)

        self._toggle_button = Gtk.Button(label='Start Sharing')
        self._toggle_button.add_css_class('suggested-action')
        self._toggle_button.add_css_class('pill')
        self._toggle_button.set_halign(Gtk.Align.CENTER)
        self._toggle_button.set_margin_top(8)
        self._toggle_button.connect('clicked', self._on_toggle_sharing)

        content.append(status_group)
        content.append(self._toggle_button)

        # Account info
        account_group = Adw.PreferencesGroup(title='Account')

        self._account_row = Adw.ActionRow(
            title='Logged in as',
            subtitle='—',
        )
        account_icon = Gtk.Image.new_from_icon_name('avatar-default-symbolic')
        self._account_row.add_prefix(account_icon)
        status_group.add(self._account_row)

        logout_button = Gtk.Button(
            icon_name='system-log-out-symbolic',
            valign=Gtk.Align.CENTER,
            tooltip_text='Sign Out',
        )
        logout_button.add_css_class('flat')
        logout_button.connect('clicked', self._on_logout_clicked)
        self._account_row.add_suffix(logout_button)

        content.append(account_group)

        clamp.set_child(content)
        page_box.append(clamp)

        self._view_stack.add_named(page_box, 'dashboard')

    # ── Download Logic ───────────────────────────────────────────────

    def _check_cli_binary(self):
        if self._cli_manager.is_cli_available():
            self._on_download_complete()
        else:
            self._view_stack.set_visible_child_name('download')
            downloader = PawnsCLIDownloader()
            downloader.download_async(self._on_download_finished)

    def _on_download_finished(self, success, error_msg):
        GLib.idle_add(self._handle_download_result, success, error_msg)

    def _handle_download_result(self, success, error_msg):
        self._download_spinner.set_spinning(False)
        if success:
            self._on_download_complete()
        else:
            toast = Adw.Toast(title=f'Download failed: {error_msg}', timeout=5)
            self._toast_overlay.add_toast(toast)
            # Add retry button
            retry_btn = Gtk.Button(label='Retry Download')
            retry_btn.add_css_class('suggested-action')
            retry_btn.add_css_class('pill')
            retry_btn.set_halign(Gtk.Align.CENTER)
            retry_btn.connect('clicked', lambda b: self._retry_download())
            page = self._view_stack.get_child_by_name('download')
            page.set_child(retry_btn)
            page.set_description('Download failed. Please check your connection.')
        return GLib.SOURCE_REMOVE

    def _retry_download(self):
        page = self._view_stack.get_child_by_name('download')
        page.set_description('Please wait while the CLI tool is being downloaded…')
        self._download_spinner.set_spinning(True)
        page.set_child(self._download_spinner)
        downloader = PawnsCLIDownloader()
        downloader.download_async(self._on_download_finished)

    def _on_download_complete(self):
        saved_email = self._settings.get_string('email')
        saved_device = self._settings.get_string('device-name')

        if saved_email and saved_device:
            self._show_login_page()
        else:
            self._show_login_page()

    def _show_login_page(self):
        self._view_stack.set_visible_child_name('login')

    # ── Login Logic ──────────────────────────────────────────────────

    def _on_login_clicked(self, _button):
        email = self._email_row.get_text().strip()
        password = self._password_row.get_text().strip()
        device = self._device_row.get_text().strip()

        if not email:
            self._show_toast('Please enter your email address.')
            return
        if not password:
            self._show_toast('Please enter your password.')
            return
        if not device:
            self._show_toast('Please enter a device name.')
            return

        # Save settings (not password)
        self._settings.set_string('email', email)
        self._settings.set_string('device-name', device)
        self._password = password

        self._show_dashboard(email)

        # Auto-start if enabled
        if self._settings.get_boolean('autostart-sharing'):
            self._start_sharing()

    def _show_dashboard(self, email):
        self._account_row.set_subtitle(email)
        self._view_stack.set_visible_child_name('dashboard')
        self._show_toast('Signed in successfully.')

    # ── Dashboard Logic ──────────────────────────────────────────────

    def _on_toggle_sharing(self, _button):
        if self._cli_manager.is_running():
            self._stop_sharing()
        else:
            self._start_sharing()

    def _start_sharing(self):
        email = self._settings.get_string('email')
        device = self._settings.get_string('device-name')
        password = self._password

        if not password:
            self._show_toast('Please sign in again to start sharing.')
            self._view_stack.set_visible_child_name('login')
            return

        success = self._cli_manager.start(email, password, device)
        if success:
            self._update_status(running=True)
            self._show_toast('Internet sharing started.')
        else:
            self._show_toast('Failed to start Pawns CLI.')

    def _stop_sharing(self):
        self._cli_manager.stop()
        self._update_status(running=False)
        self._show_toast('Internet sharing stopped.')

    def _update_status(self, running):
        if running:
            self._status_row.set_subtitle('Running')
            self._status_icon.set_from_icon_name('media-playback-start-symbolic')
            self._toggle_button.set_label('Stop Sharing')
            self._toggle_button.remove_css_class('suggested-action')
            self._toggle_button.add_css_class('destructive-action')
        else:
            self._status_row.set_subtitle('Stopped')
            self._status_icon.set_from_icon_name('media-playback-stop-symbolic')
            self._toggle_button.set_label('Start Sharing')
            self._toggle_button.remove_css_class('destructive-action')
            self._toggle_button.add_css_class('suggested-action')

    def _on_logout_clicked(self, _button):
        self._cli_manager.stop()
        self._password = ''
        self._settings.set_string('email', '')
        self._update_status(running=False)
        self._password_row.set_text('')
        self._view_stack.set_visible_child_name('login')
        self._show_toast('Signed out.')

    # ── Helpers ──────────────────────────────────────────────────────

    def _show_toast(self, message):
        toast = Adw.Toast(title=message, timeout=3)
        self._toast_overlay.add_toast(toast)
