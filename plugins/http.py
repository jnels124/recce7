from plugins.base import BasePlugin
from socket import SocketIO
from socket import timeout
from http.server import BaseHTTPRequestHandler

PAGE_LOGIN = b"""<html>
    <head>
        <style>
            form {
                text-align: center;
            }
        </style>
        <section class="loginform cf">
        <form action="login" method="post">
            Username<br>
            <input type="text" name="username" required><br>
            Password<br>
            <input type="password" name="password" required><br>
            <input type="submit" value="Login">
        </form>
        </section>
    </head>
</html>"""

MAX_MESSAGE_LENGTH = 65536

class HTTPPlugin(BasePlugin, BaseHTTPRequestHandler):
    def __init__(self, socket, config, framework):
        BasePlugin.__init__(self, socket, config, framework)

        self.rfile = SocketIO(socket, "r")
        self.wfile = SocketIO(socket, "w")

        self.command = None
        self.path = None
        self.headers = None
        self.body = None

        socket.settimeout(60)

    def do_track(self):
        self.handle_one_request()
        self.write_data()

        self._skt = None

    def get_body(self):
        too_long = False

        if self.headers == None:
            self.body = ''
            return
        else:

            try:
                body_length = int(self.headers.get('content-length', 0))
                if body_length > 65536:
                    body_length = 65536
                    too_long = True
            except TypeError:
                self.body = ''
                return

            try:
                self.body = self.rfile.read(body_length)
                self.body = str(self.body, 'utf-8')
                if too_long:
                    self.body += '*'
            except timeout:
                self.body = ''

        print(self.body)

    def write_data(self):
        if self.command == None:
            self.command = ''
        if self.path == None:
            self.path = ''
        if self.headers == None:
            self.headers = ''
        else:
            self.headers = self.headers.as_string()
        if self.body == None:
            self.body = ''

        entry = {'test_http': {'METHOD' : self.command,
                               'PATH' : self.path,
                               'HEADERS' : self.headers,
                               'BODY' : self.body}}

        self.do_save(entry)

    def address_string(self):
        return self._skt.getpeername()[0]

    def do_GET(self):
        self.do_HEAD()
        if self.path == '/':
            self.wfile.write(PAGE_LOGIN)

    def do_HEAD(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(PAGE_LOGIN)))
            self.end_headers()
        elif self.path == '/login':
            self.send_error(403)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path =='/':
            self.do_GET()
        if self.path == '/login':
            self.send_error(500)
            self.get_body()
        else:
            self.send_error(404)
            self.get_body()

    def do_PUT(self):
        '''self.send_response(100)
        self.end_headers()
        self.get_body()'''
        self.send_error(501)