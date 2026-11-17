"""Serve the dashboard over a loopback-only HTTP connection."""

from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


STATIC = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/styles.css": ("styles.css", "text/css; charset=utf-8"),
    "/dashboard.js": ("dashboard.js", "text/javascript; charset=utf-8"),
}
CONTENT_POLICY = (
    "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
    "connect-src 'self'; img-src 'self' data:; font-src 'self'; "
    "frame-ancestors 'none'; base-uri 'none'; form-action 'none'"
)
WEB_ROOT = Path(__file__).resolve().parent / "web"


class DashboardServer(ThreadingHTTPServer):
    def __init__(self, provider, port, web_root):
        self.provider = provider
        self.web_root = web_root
        super().__init__(("127.0.0.1", port), DashboardHandler)

    def handle_error(self, request, client_address):
        # The standard handler prints uncaught exceptions, which can contain MT5 identifiers.
        pass


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "MT5Dashboard"
    sys_version = ""
    timeout = 5

    def log_message(self, format, *args):
        # Request paths and header values can contain account information.
        pass

    def _trusted_request(self):
        port = self.server.server_port
        hosts = self.headers.get_all("Host", [])
        if len(hosts) != 1:
            return False
        host = hosts[0].lower()
        allowed_hosts = {"127.0.0.1", "localhost", f"127.0.0.1:{port}", f"localhost:{port}"}
        if host not in allowed_hosts:
            return False
        origin = self.headers.get("Origin")
        if origin is not None and origin.lower() != f"http://{host}":
            return False
        return self.headers.get("Sec-Fetch-Site") in (None, "none", "same-origin")

    def _respond(self, status, content_type, body):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", CONTENT_POLICY)
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _plain(self, status, message):
        self._respond(status, "text/plain; charset=utf-8", message.encode("utf-8"))

    def do_GET(self):
        if not self._trusted_request():
            self._plain(HTTPStatus.FORBIDDEN, "Open the dashboard from its local address.")
            return

        # BaseHTTPRequestHandler normalizes an initial double slash. Require the literal route.
        path = self.requestline.split()[1]
        if path == "/api/snapshot":
            snapshot = self.server.provider.snapshot()
            body = json.dumps(snapshot, allow_nan=False, separators=(",", ":")).encode("utf-8")
            self._respond(HTTPStatus.OK, "application/json; charset=utf-8", body)
            return

        if path not in STATIC:
            self._plain(HTTPStatus.NOT_FOUND, "Page not found.")
            return

        filename, content_type = STATIC[path]
        try:
            body = (self.server.web_root / filename).read_bytes()
        except OSError:
            self._plain(HTTPStatus.NOT_FOUND, "Dashboard asset is unavailable.")
            return
        self._respond(HTTPStatus.OK, content_type, body)


def create_server(provider, port=8765, *, web_root=WEB_ROOT):
    return DashboardServer(provider, port, web_root)
