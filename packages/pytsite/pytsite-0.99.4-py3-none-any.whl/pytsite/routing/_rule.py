"""PytSite Routing Rule
"""
import re as _re
from pytsite import util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_rule_arg_re = _re.compile('<(?:(\w+)(?:\(([\w\|]*)\))?:)?(\w+)>')
_parametrized_arg_type_re = _re.compile('(\w+)\(([\w\|]*)\)')


def _rule_arg_repl_func(match):
    arg_formatter = match.group(1) or 'common'
    arg_formatter_params_str = match.group(2) or ''
    arg_formatter_params = arg_formatter_params_str.split('|') if arg_formatter_params_str else []
    arg_name = match.group(3)

    if arg_formatter == 'common':
        return '(?P<{}>[^/]+)'.format(arg_name)
    elif arg_formatter == 'int':
        return '(?P<{}>\d+)'.format(arg_name)
    elif arg_formatter == 'float':
        return '(?P<{}>\d+\.\d+)'.format(arg_name)
    elif arg_formatter == 'alpha':
        return '(?P<{}>[a-z-A-Z]+)'.format(arg_name)
    elif arg_formatter == 'alnum':
        return '(?P<{}>[a-z-A-Z0-9]+)'.format(arg_name)
    elif arg_formatter == 'hex':
        return '(?P<{}>[0-9a-fA-F]+)'.format(arg_name)
    elif arg_formatter == 'choice':
        if not arg_formatter_params:
            raise _error.RuleArgumentError("Argument formatter '{}' expects parameters".format(arg_formatter))
        return '(?P<{}>({}))'.format(arg_name, '|'.join(arg_formatter_params))
    elif arg_formatter == 'path':
        return '(?P<{}>.+)'.format(arg_name)
    else:
        raise _error.RuleArgumentError('Unknown rule argument formatter: {}'.format(arg_formatter))


class Rule:
    """Routing Rule
    """

    def __init__(self, path: str, handler, name: str = None, defaults: dict = None, methods='GET', attrs: dict = None):
        if not path.startswith('/'):
            path = '/' + path

        if path.endswith('/'):
            path = path[:-1]

        if not name:
            name = _util.random_str()

        if isinstance(methods, str):
            if methods == '*':
                methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']
            else:
                methods = [methods]

        self._path = path
        self._handler = handler
        self._name = name
        self._method = set([m.upper() for m in methods])
        self._attrs = attrs if attrs else {}

        # Build regular expression
        rule_regex_str = _rule_arg_re.sub(_rule_arg_repl_func, path)
        self._regex = _re.compile('^/?{}/?$'.format(rule_regex_str))

        # Build arguments dictionary based on regular expression
        self._args = dict.fromkeys(self._regex.groupindex.keys())

        # Fill arguments with defaults
        if defaults:
            self._args.update(defaults)

    @property
    def path(self) -> str:
        return self._path

    @property
    def handler(self):
        return self._handler

    @property
    def name(self) -> str:
        return self._name

    @property
    def methods(self) -> set:
        return self._method

    @property
    def attrs(self) -> dict:
        return self._attrs

    @property
    def regex(self):
        return self._regex

    @property
    def args(self) -> dict:
        return self._args
