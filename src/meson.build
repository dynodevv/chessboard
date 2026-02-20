pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'chessboard'

python_sources = [
  '__init__.py',
  'main.py',
  'application.py',
  'window.py',
  'download.py',
  'cli_manager.py',
  'preferences.py',
]

install_data(python_sources, install_dir: moduledir)

configure_file(
  input: 'chessboard.in',
  output: 'chessboard',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)
