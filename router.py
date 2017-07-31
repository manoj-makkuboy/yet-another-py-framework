import re
import pdb
from webob import Request, exc


def template_to_regex(template):
    var_regex = re.compile(r'''
        \{           # The exact character {
        (\w+)       # The variable name (restricted to a-z, 0-9, _)
        (?::([^}]+))? # The optional : regext part
        \}          # The exact character "}"
        ''', re.VERBOSE)

    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex


def load_controller(string):
    module_name, func_name = string.split(':', 1)
    imported_module = __import__(module_name)
    imported_function = getattr(imported_module, func_name)
    return imported_function


class Router(object):
    def __init__(self):
        self.routes = []

    def add_route(self, template, controller):
        if isinstance(controller, str):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),
                           controller),)

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller in self.routes:
            match = regex.match(req.path_info)
            if match:
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)
