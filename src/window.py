import os
from datetime import datetime

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Secret', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Secret

from process_manager import ProcessManager

SECRET_SCHEMA = Secret.Schema.new(
    "org.dynodevv.chessboard.Credentials",
    Secret.SchemaFlags.NONE,
    {"email": Secret.SchemaAttributeType.STRING},
)

SETTINGS_SCHEMA = "org.dynodevv.chessboard"


class ChessboardWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(450, 600)
        self.set_title("Chessboard")

        self._process_manager = ProcessManager(self._on_process_died)
        self._settings = Gio.Settings.new(SETTINGS_SCHEMA)
        self._email = None

        self._build_ui()
        self._try_auto_login()

    def _build_ui(self):
        self._view_stack = Adw.ViewStack()

        # --- Header bar ---
        menu_model = Gio.Menu()
        menu_model.append("About", "app.about")
        menu_model.append("Quit", "app.quit")

        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        menu_button.set_menu_model(menu_model)

        header = Adw.HeaderBar()
        header.pack_end(menu_button)

        # --- Login view ---
        self._email_row = Adw.EntryRow(title="Email")
        self._email_row.set_input_purpose(Gtk.InputPurpose.EMAIL)

        self._password_row = Adw.PasswordEntryRow(title="Password")

        sign_in_button = Gtk.Button(label="Sign In")
        sign_in_button.add_css_class("suggested-action")
        sign_in_button.add_css_class("pill")
        sign_in_button.set_margin_top(24)
        sign_in_button.connect("clicked", self._on_sign_in)

        twofa_label = Gtk.Label(
            label="2FA is not supported by the Pawns.app CLI.\n"
                  "Please disable it in your account to use Chessboard.",
        )
        twofa_label.add_css_class("dim-label")
        twofa_label.add_css_class("caption")
        twofa_label.set_wrap(True)
        twofa_label.set_justify(Gtk.Justification.CENTER)
        twofa_label.set_margin_top(8)

        login_group = Adw.PreferencesGroup()
        login_group.add(self._email_row)
        login_group.add(self._password_row)

        login_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        login_box.set_margin_start(24)
        login_box.set_margin_end(24)
        login_box.append(login_group)
        login_box.append(sign_in_button)
        login_box.append(twofa_label)

        login_clamp = Adw.Clamp()
        login_clamp.set_maximum_size(360)
        login_clamp.set_child(login_box)

        login_page = Adw.StatusPage()
        login_page.set_title("Chessboard")
        login_page.set_description("Sign in to your Pawns.app account")
        login_page.set_icon_name("org.dynodevv.chessboard")
        login_page.set_child(login_clamp)

        self._view_stack.add_titled(login_page, "login", "Login")

        # --- Home view ---
        self._sharing_switch = Gtk.Switch()
        self._sharing_switch.set_valign(Gtk.Align.CENTER)
        self._sharing_switch.connect("state-set", self._on_sharing_toggled)

        self._sharing_row = Adw.ActionRow(
            title="Internet Sharing",
            subtitle="Inactive",
        )
        self._sharing_row.add_suffix(self._sharing_switch)
        self._sharing_row.set_activatable_widget(self._sharing_switch)

        dashboard_row = Adw.ActionRow(
            title="Open Dashboard",
            subtitle="View your Pawns.app dashboard",
            activatable=True,
        )
        dashboard_row.add_suffix(
            Gtk.Image.new_from_icon_name("go-next-symbolic")
        )
        dashboard_row.connect("activated", self._on_open_dashboard)

        home_group = Adw.PreferencesGroup()
        home_group.add(self._sharing_row)
        home_group.add(dashboard_row)

        # --- Settings group ---
        self._logging_switch = Gtk.Switch()
        self._logging_switch.set_valign(Gtk.Align.CENTER)
        self._settings.bind(
            "logging-enabled",
            self._logging_switch,
            "active",
            Gio.SettingsBindFlags.DEFAULT,
        )

        logging_row = Adw.ActionRow(
            title="Enable Logging",
            subtitle="Save pawns-cli output to log files",
        )
        logging_row.add_suffix(self._logging_switch)
        logging_row.set_activatable_widget(self._logging_switch)

        open_logs_row = Adw.ActionRow(
            title="Open Logs Folder",
            activatable=True,
        )
        open_logs_row.add_suffix(
            Gtk.Image.new_from_icon_name("folder-open-symbolic")
        )
        open_logs_row.connect("activated", self._on_open_logs)

        settings_group = Adw.PreferencesGroup(title="Settings")
        settings_group.add(logging_row)
        settings_group.add(open_logs_row)

        # --- Account group ---
        sign_out_row = Adw.ActionRow(
            title="Sign Out",
            activatable=True,
        )
        sign_out_row.add_css_class("error")
        sign_out_row.connect("activated", self._on_sign_out)

        account_group = Adw.PreferencesGroup()
        account_group.add(sign_out_row)

        home_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        home_box.set_margin_start(24)
        home_box.set_margin_end(24)
        home_box.append(home_group)
        home_box.append(settings_group)
        home_box.append(account_group)

        home_clamp = Adw.Clamp()
        home_clamp.set_maximum_size(360)
        home_clamp.set_child(home_box)

        home_page = Adw.StatusPage()
        home_page.set_title("Chessboard")
        home_page.set_description("Manage your internet sharing")
        home_page.set_icon_name("org.dynodevv.chessboard")
        home_page.set_child(home_clamp)

        self._view_stack.add_titled(home_page, "home", "Home")

        # --- Main layout ---
        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(header)
        toolbar.set_content(self._view_stack)

        self.set_content(toolbar)

    # --- Credential helpers ---

    def _store_credentials(self, email, password):
        Secret.password_store_sync(
            SECRET_SCHEMA,
            {"email": email},
            Secret.COLLECTION_DEFAULT,
            "Chessboard Pawns.app credentials",
            password,
            None,
        )
        self._settings.set_string("last-email", email)

    def _lookup_credentials(self):
        email = self._settings.get_string("last-email")
        if not email:
            return None
        password = Secret.password_lookup_sync(
            SECRET_SCHEMA, {"email": email}, None
        )
        if password:
            return (email, password)
        return None

    def _clear_credentials(self):
        if self._email:
            Secret.password_clear_sync(
                SECRET_SCHEMA, {"email": self._email}, None
            )
        self._settings.set_string("last-email", "")

    # --- Log helpers ---

    def _get_log_dir(self):
        log_dir = os.path.join(GLib.get_user_data_dir(), "chessboard", "logs")
        os.makedirs(log_dir, exist_ok=True)
        return log_dir

    def _get_log_file_path(self):
        log_dir = self._get_log_dir()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return os.path.join(log_dir, f"pawns-cli-{timestamp}.log")

    # --- Status helpers ---

    def _update_sharing_status(self, active):
        if active:
            self._sharing_row.set_subtitle("Active")
        else:
            self._sharing_row.set_subtitle("Inactive")

    # --- Auto-login ---

    def _try_auto_login(self):
        creds = self._lookup_credentials()
        if creds:
            self._email = creds[0]
            self._view_stack.set_visible_child_name("home")

    # --- Signal handlers ---

    def _on_sign_in(self, button):
        email = self._email_row.get_text().strip()
        password = self._password_row.get_text().strip()

        if not email or not password:
            return

        self._email = email
        self._store_credentials(email, password)
        self._email_row.set_text("")
        self._password_row.set_text("")

        self._view_stack.set_visible_child_name("home")

    def _on_sharing_toggled(self, switch, state):
        if state:
            creds = self._lookup_credentials()
            if creds:
                log_path = None
                if self._settings.get_boolean("logging-enabled"):
                    log_path = self._get_log_file_path()
                success = self._process_manager.start(
                    creds[0], creds[1], log_file=log_path
                )
                if success:
                    switch.set_state(True)
                    self._update_sharing_status(True)
                else:
                    switch.set_active(False)
                    self._update_sharing_status(False)
            else:
                switch.set_active(False)
        else:
            self._process_manager.stop()
            switch.set_state(False)
            self._update_sharing_status(False)
        return True

    def _on_process_died(self):
        self._sharing_switch.set_active(False)
        self._sharing_switch.set_state(False)
        self._update_sharing_status(False)

    def _on_open_dashboard(self, row):
        Gtk.show_uri(self, "https://dashboard.pawns.app", 0)

    def _on_open_logs(self, row):
        log_dir = self._get_log_dir()
        Gtk.show_uri(self, GLib.filename_to_uri(log_dir, None), 0)

    def _on_sign_out(self, row):
        self._process_manager.stop()
        self._sharing_switch.set_active(False)
        self._sharing_switch.set_state(False)
        self._update_sharing_status(False)
        self._clear_credentials()
        self._email = None
        self._view_stack.set_visible_child_name("login")
