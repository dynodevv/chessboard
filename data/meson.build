install_data(
  'org.dynodevv.chessboard.desktop.in',
  rename: 'org.dynodevv.chessboard.desktop',
  install_dir: join_paths(get_option('datadir'), 'applications'),
)

install_data(
  'org.dynodevv.chessboard.metainfo.xml.in',
  rename: 'org.dynodevv.chessboard.metainfo.xml',
  install_dir: join_paths(get_option('datadir'), 'metainfo'),
)

install_data(
  'org.dynodevv.chessboard.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0', 'schemas'),
)

gnome.compile_schemas(depend_files: 'org.dynodevv.chessboard.gschema.xml')

install_subdir(
  'icons',
  install_dir: join_paths(get_option('datadir')),
)
