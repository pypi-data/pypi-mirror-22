
import sys
import traceback
import logging

import ujson

from nanohttp.contexts import Context, context
from nanohttp.exceptions import HttpStatus, InternalServerError
from nanohttp.configuration import settings


logger = logging.getLogger('nanohttp')


class Application:
    __logger__ = logger
    __root__ = None

    def __init__(self, root=None):
        self.__root__ = root
        self._hook('app_init')

    def _hook(self, name, *args, **kwargs):
        if hasattr(self, name):
            return getattr(self, name)(*args, **kwargs)

    def _handle_exception(self, ex):
        context.response_encoding = 'utf-8'

        error = ex if isinstance(ex, HttpStatus) else InternalServerError(sys.exc_info())
        error_page = self._hook('request_error', error)
        message = error.status_text
        description = error.render() if settings.debug else error.info if error_page is None else error_page

        if context.response_content_type == 'application/json':
            response = ujson.encode(dict(
                message=message,
                description=description
            ))
        else:
            context.response_content_type = 'text/plain'
            response = "%s\n%s" % (message, description)

        if isinstance(error, InternalServerError):
            traceback.print_exc()

        def resp():
            yield response

        return error.status, resp()

    def __call__(self, environ, start_response):
        ctx = Context(environ)
        ctx.__enter__()
        # start_response("200 OK", [('Content-Type', 'text/plain; charset=utf-8')])

        status = '200 OK'
        buffer = None

        try:
            self._hook('begin_request')
            if self.__root__.__remove_trailing_slash__:
                ctx.path = ctx.path.rstrip('/')

            result = self.__root__(*ctx.path.split('?')[0][1:].split('/'))
            if result:
                resp_generator = iter(result)
                buffer = next(resp_generator)
            else:
                resp_generator = None

        except Exception as ex:
            self.__logger__.exception('Exception while handling the request.')
            status, resp_generator = self._handle_exception(ex)

        finally:
            self._hook('begin_response')

            if context.response_cookies:
                for cookie in context.response_cookies:
                    ctx.response_headers.add_header(*cookie.http_set_cookie())
            start_response(status, ctx.response_headers.items())

        def _response():
            try:
                if buffer is not None:
                    yield ctx.encode_response(buffer)

                if resp_generator:
                    # noinspection PyTypeChecker
                    for chunk in resp_generator:
                        yield ctx.encode_response(chunk)
                else:
                    yield b''
            except Exception as ex_:  # pragma: no cover
                self.__logger__.exception('Exception while serving the response.')
                if settings.debug:
                    yield str(ex_).encode()
                raise ex_

            finally:
                self._hook('end_response')
                context.__exit__(*sys.exc_info())

        return _response()
