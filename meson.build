project('chessboard',
  version: '1.0.0',
  license: 'MIT',
  meson_version: '>= 0.59.0',
)

app_id = 'org.dynodevv.chessboard'

gnome = import('gnome')

subdir('src')
subdir('data')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
