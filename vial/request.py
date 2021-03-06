import json
import urllib.parse

from .route import VRoute
from .utils import CaseInsensitiveDict


class VRequestBody():
    def __init__(self, request):
        self.request = request

    def read(self, *args, **kwargs):
        return self.file.read(*args, **kwargs)

    @property
    def file(self):
        return self.request["wsgi.input"]

    @property
    def raw(self):
        length = self.request.length
        if not length:
            return b""
        return self.file.read(length)

    @property
    def json(self):
        body = self.raw
        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}

    @property
    def text(self):
        return self.raw.decode("utf-8")


class VRequest():
    def __init__(self, environ):
        self.environ = environ
        self.body = VRequestBody(self)

    def __repr__(self):
        return f"<{self.method} Request '{self.path}'>"

    def __getitem__(self, key):
        return self.environ[key]

    @property
    def headers(self):
        if not hasattr(self, "_headers"):
            self._headers = CaseInsensitiveDict()
            for key, value in self.environ.items():
                key = key.lower()
                if not key.startswith("http_"):
                    continue
                key = key.replace("http_", "", 1).replace("_", "-")
                self._headers[key] = value
        return self._headers

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"]

    @property
    def path(self):
        return self.environ["PATH_INFO"]

    @property
    def pathlist(self):
        return [r for r in self.path.split("/") if r]

    @property
    def query_string(self):
        return self.environ["QUERY_STRING"]

    @property
    def query(self):
        if not hasattr(self, "_query"):
            self._query = urllib.parse.parse_qs(self.query_string)
        return self._query

    @property
    def length(self):
        try:
            return int(self.environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            return 0

    @property
    def host(self):
        return self.environ["HTTP_HOST"]

    @property
    def connection(self):
        return self.environ.get("HTTP_CONNECTION")

    @property
    def cache_control(self):
        return self.environ.get("HTTP_CACHE_CONTROL")

    @property
    def user_agent(self):
        return self.environ.get("HTTP_USER_AGENT")

    @property
    def accept(self):
        return self.environ["HTTP_ACCEPT"]

    @property
    def accept_encoding(self):
        return self.environ.get("HTTP_ACCEPT_ENCODING")

    @property
    def accept_language(self):
        return self.environ.get("HTTP_ACCEPT_LANGUAGE")

    def route(self, *args):
        return VRoute(self, *args)
