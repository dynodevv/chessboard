project('chessboard',
  version: '1.0.0',
  meson_version: '>= 0.62.0',
  default_options: ['warning_level=2'],
)

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

py_installation = python.find_installation('python3')

app_id = 'org.dynodevv.chessboard'
pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('VERSION', meson.project_version())
conf.set('APP_ID', app_id)
conf.set('pkgdatadir', pkgdatadir)
conf.set('localedir', get_option('prefix') / get_option('localedir'))

subdir('data')
subdir('src')
