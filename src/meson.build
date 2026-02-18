pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

conf = configuration_data()
conf.set('pkgdatadir', pkgdatadir)
conf.set('VERSION', meson.project_version())

configure_file(
  input: 'chessboard.in',
  output: 'chessboard',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x',
)

sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'process_manager.py',
]

install_data(sources, install_dir: pkgdatadir)
