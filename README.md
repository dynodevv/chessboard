# Chessboard

A premium Linux client for [Pawns.app](https://pawns.app) CLI, built with GTK4 and Libadwaita.

![Screenshot placeholder](https://via.placeholder.com/450x600?text=Chessboard)

## Features

- **Native GNOME experience** — built with GTK4 and Libadwaita following the GNOME HIG
- **Secure credential storage** — passwords are stored using libsecret (GNOME Keyring)
- **One-click sharing** — start and stop internet sharing with a single toggle
- **Process monitoring** — automatically detects when the pawns-cli process stops
- **Dashboard access** — quickly open the Pawns.app dashboard from the app

## Requirements

- Python 3
- GTK 4
- Libadwaita 1.2+
- libsecret
- [pawns-cli](https://pawns.app) binary in your `PATH` or working directory

## Building from Source

```bash
meson setup builddir
ninja -C builddir
sudo ninja -C builddir install
```

## Flatpak

```bash
cd flatpak
flatpak-builder --user --install --force-clean build-dir org.dynodevv.chessboard.json
```

## Legal Disclaimer

This project is **not** associated with, nor endorsed by, IPRoyal. Pawns.app and
IPRoyal are trademarks of their respective owners. Use this software at your own risk.

## License

This project is licensed under the [MIT License](LICENSE).
