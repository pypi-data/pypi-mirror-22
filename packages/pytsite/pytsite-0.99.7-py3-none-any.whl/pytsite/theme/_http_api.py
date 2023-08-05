"""PytSite Theme HTTP API.
"""
from pytsite import auth as _auth, http as _http
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def get_settings(inp: dict, theme_package_name: str):
    if not _auth.get_current_user().has_permission('pytsite.theme.manage'):
        raise _http.error.Forbidden()

    r = []

    try:
        theme = _api.get(theme_package_name)

        if not theme.is_loaded:
            theme.load()

        for w in theme.package.get_settings_widgets():
            setting_val = theme.settings.get(w.uid)
            if setting_val:
                w.value = setting_val

            w.uid = 'setting_theme_{}_{}'.format(theme.name, w.uid).replace('.', '_')
            w.name = 'setting_theme_{}[{}]'.format(theme.name, w.name)

            r.append(w.render())

    except AttributeError:
        # Theme may not define get_settings_widget()
        pass

    return r
