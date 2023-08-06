import json

from clink.error.http import HttpError, code_to_str
from clink.iface import IErrorHandler
from clink.mime.type import MIME_JSON
from clink.com.marker import com
from clink.type.com import AppErrHandler


@com()
class ErrorHttpHandler(AppErrHandler, IErrorHandler):
    def handle(self, req, res, e):
        if not isinstance(e, HttpError):
            return False
        res.status = e.status
        res.header = {}
        res.content_type = MIME_JSON
        res.body = json.dumps({
            'status': e.status,
            'status_name': code_to_str(e.status),
            'message': e.msg
        }).encode('utf-8')
        return True
