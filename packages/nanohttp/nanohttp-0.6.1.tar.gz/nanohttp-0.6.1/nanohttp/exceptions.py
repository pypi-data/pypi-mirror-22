
from .contexts import context


class HttpStatus(Exception):
    status_code = None
    status_text = None
    info = None

    def __init__(self, message=None, reason=None):
        if reason:
            context.response_headers.add_header('X-Reason', reason)
        super().__init__(message or self.status_text)

    @property
    def status(self):
        return '%s %s' % (self.status_code, self)

    def render(self):
        return self.status


class HttpBadRequest(HttpStatus):
    status_code, status_text, info = 400, 'Bad Request', 'Bad request syntax or unsupported method'


class HttpUnauthorized(HttpStatus):
    status_code, status_text, info = 401, 'Unauthorized', 'No permission -- see authorization schemes'


class HttpForbidden(HttpStatus):
    status_code, status_text, info = 403, 'Forbidden', 'Request forbidden -- authorization will not help'


class HttpNotFound(HttpStatus):
    status_code, status_text, info = 404, 'Not Found', 'Nothing matches the given URI'


class HttpMethodNotAllowed(HttpStatus):
    status_code, status_text, info = 405, 'Method Not Allowed', 'Specified method is invalid for this resource'


class HttpConflict(HttpStatus):
    status_code, status_text, info = 409, 'Conflict', 'Request conflict'


class HttpGone(HttpStatus):
    status_code, status_text, info = 410, 'Gone', 'URI no longer exists and has been permanently removed'


class HttpRedirect(HttpStatus):

    def __init__(self, location, *args, **kw):
        context.response_headers.add_header('Location', location)
        super().__init__(*args, **kw)


class HttpMovedPermanently(HttpRedirect):
    status_code, status_text, info = 301, 'Moved Permanently', 'Object moved permanently -- see URI list'


class HttpFound(HttpRedirect):
    status_code, status_text, info = 302, 'Found', 'Object moved temporarily -- see URI list'


# FIXME: Rename to HttpInternalServerError
class InternalServerError(HttpStatus):
    status_code, status_text, info = 500, 'Internal Server Error', 'Server got itself in trouble'

    def __init__(self, exc_info):
        self.exc_info = exc_info

    def render(self):
        from traceback import format_tb
        e_type, e_value, tb = self.exc_info
        return 'Traceback (most recent call last):\n%s\n%s: %s' % (
            ''.join(format_tb(tb)),
            e_type.__name__,
            e_value
        )
