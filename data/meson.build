desktop_file = i18n.merge_file(
  input: 'org.dynodevv.chessboard.desktop.in',
  output: 'org.dynodevv.chessboard.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'applications',
)

appstream_file = i18n.merge_file(
  input: 'org.dynodevv.chessboard.metainfo.xml.in',
  output: 'org.dynodevv.chessboard.metainfo.xml',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'metainfo',
)

install_data(
  'org.dynodevv.chessboard.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas',
)

gnome.compile_schemas(depend_files: 'org.dynodevv.chessboard.gschema.xml')

gnome.compile_resources('chessboard',
  'chessboard.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

icondir = get_option('datadir') / 'icons' / 'hicolor'

install_data(
  'icons' / 'hicolor' / 'scalable' / 'apps' / 'org.dynodevv.chessboard.svg',
  install_dir: icondir / 'scalable' / 'apps',
)

install_data(
  'icons' / 'hicolor' / 'symbolic' / 'apps' / 'org.dynodevv.chessboard-symbolic.svg',
  install_dir: icondir / 'symbolic' / 'apps',
)
