
from os.path import isdir, join
import threading

import pymlconf

from .configuration import settings


class LazyAttribute(object):
    """ ``attribute`` decorator is intended to promote a
        function call to object attribute. This means the
        function is called once and replaced with
        returned value.

        >>> class A:
        ...     def __init__(self):
        ...         self.counter = 0
        ...     @LazyAttribute
        ...     def count(self):
        ...         self.counter += 1
        ...         return self.counter
        >>> a = A()
        >>> a.count
        1
        >>> a.count
        1
    """
    __slots__ = ('f', )

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, t=None):
        f = self.f
        val = f(obj)
        setattr(obj, f.__name__, val)
        return val


def load_controller_from_file(specifier):
    from importlib.util import spec_from_file_location, module_from_spec
    controller = None

    if specifier:
        module_name, class_name = specifier.split(':') if ':' in specifier else (specifier, 'Root')

        if module_name:

            if isdir(module_name):
                location = join(module_name, '__init__.py')
            elif module_name.endswith('.py'):
                location = module_name
                module_name = module_name[:-3]
            else:
                location = '%s.py' % module_name

            spec = spec_from_file_location(module_name, location=location)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            controller = getattr(module, class_name)()

        elif class_name == 'Static':
            from .controllers import Static
            controller = Static()
        else:  # pragma: no coverg
            controller = globals()[class_name]()

    return controller


def quickstart(controller=None, host='localhost',  port=8080, block=True, config=None):
    from wsgiref.simple_server import make_server

    try:
        settings.proxied_object
    except pymlconf.ConfigurationNotInitializedError:
        settings.load()

    if config:
        settings.merge(config)

    if controller is None:
        from wsgiref.simple_server import demo_app
        app = demo_app
    else:
        app = controller.load_app()

    port = int(port)
    httpd = make_server(host, port, app)

    print("Serving http://%s:%d" % (host or 'localhost', port))
    if block:  # pragma: no cover
        httpd.serve_forever()
    else:
        t = threading.Thread(target=httpd.serve_forever, daemon=True)
        t.start()

        def shutdown():
            httpd.shutdown()
            httpd.server_close()
            t.join()

        return shutdown
