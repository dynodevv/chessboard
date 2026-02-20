# Chessboard

A premium Linux client for [IPRoyal's Pawns.app](https://pawns.app) CLI, built with GTK4 and Libadwaita for the modern GNOME desktop.

> **Disclaimer:** This project is not associated, nor endorsed by IPRoyal.

## Features

- **Automatic CLI Download** – Pawns CLI is downloaded automatically on first launch.
- **Simple Login** – Enter your Pawns credentials and start sharing with one click.
- **Background Process** – Pawns CLI runs silently in the background with no visible terminal.
- **Start / Stop Control** – Toggle internet sharing on and off from the dashboard.
- **Autostart Options** – Optionally auto-start sharing when Chessboard opens, or launch Chessboard at system login.
- **Modern GNOME UI** – Follows the GNOME Human Interface Guidelines using Libadwaita widgets.

## Screenshots

*Coming soon.*

## Requirements

- GNOME 45+ (GTK4, Libadwaita 1.4+)
- Python 3.11+
- PyGObject

## Building from Source

### Meson (native)

```bash
meson setup builddir
ninja -C builddir
sudo ninja -C builddir install
```

### Flatpak

```bash
flatpak-builder --user --install --force-clean build-dir flatpak/org.dynodevv.chessboard.json
```

## Project Structure

```
chessboard/
├── data/
│   ├── icons/                     # App icons (scalable + symbolic)
│   ├── chessboard.gresource.xml   # GResource bundle definition
│   ├── org.dynodevv.chessboard.desktop.in
│   ├── org.dynodevv.chessboard.gschema.xml
│   ├── org.dynodevv.chessboard.metainfo.xml.in
│   └── meson.build
├── flatpak/
│   └── org.dynodevv.chessboard.json
├── src/
│   ├── __init__.py
│   ├── application.py             # Adw.Application subclass
│   ├── chessboard.in              # Entry-point script template
│   ├── cli_manager.py             # Pawns CLI process manager
│   ├── download.py                # Async CLI downloader
│   ├── main.py                    # Bootstrap
│   ├── preferences.py             # Preferences dialog
│   ├── window.py                  # Main application window
│   └── meson.build
├── .github/
│   └── workflows/
│       └── flatpak.yml            # CI/CD Flatpak build
├── po/                            # i18n (translations)
├── LICENSE
├── README.md
└── meson.build
```

## How It Works

1. **First Launch:** Chessboard downloads the Pawns CLI binary from the official source.
2. **Sign In:** Enter your email, password, and device name. (2FA must be disabled.)
3. **Dashboard:** Start or stop internet sharing with a single button.
4. **Background:** The CLI runs as a background process with no terminal window.

## License

MIT License – see [LICENSE](LICENSE) for details.

## Author

**Dyno** — [github.com/dynodevv](https://github.com/dynodevv)
