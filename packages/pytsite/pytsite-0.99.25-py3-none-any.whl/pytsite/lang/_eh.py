"""PytSite Lang Package Event Handlers.
"""
import json as _json
from os import path as _path, makedirs as _makedirs
from pytsite import console as _console, lang as _lang, logger as _logger, reg as _reg, tpl as _tpl

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def assetman_build():
    _console.print_info(_lang.t('pytsite.assetman@compiling_translations'))

    translations = {}
    for lang_code in _lang.langs():
        translations[lang_code] = {}
        for pkg_name, info in _lang.get_packages().items():
            _logger.info("Compiling translations for {} ({})".format(pkg_name, lang_code))
            translations[lang_code][pkg_name] = _lang.load_lang_file(pkg_name, lang_code)

    # Write translations to static file
    output_file = _path.join(_reg.get('paths.static'), 'assets', 'pytsite.lang', 'translations.js')
    output_dir = _path.dirname(output_file)

    if not _path.exists(output_dir):
        _makedirs(output_dir, 0o755, True)

    with open(output_file, 'wt', encoding='utf-8') as f:
        _logger.info("Writing translations into '{}'".format(output_file))
        f.write(_tpl.render('pytsite.lang@translations-js', {
            'langs_json': _json.dumps(_lang.langs()),
            'translations_json': _json.dumps(translations),
        }))
