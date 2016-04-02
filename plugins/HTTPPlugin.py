__author__ = 'jessenelson'
__author__ = 'zkuhns'

from plugins.base import BasePlugin

import time
import urllib.parse
import socket

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

PAGE_ERROR = """<html>
    <head>
        <h1>%(error)s</h1>
    </head>
</html>"""


METHODS = {
    'GET',
    'HEAD',
    'POST',
    'PUT',
    'DELETE',
    'TRACE',
    'CONNECT'
}

DAYS = [
    'Mon',
    'Tue',
    'Wed',
    'Thu',
    'Fri',
    'Sat',
    'Sun',
]

MONTHS = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
]

STATUS_CODES = {
    100 : '100 Continue',
    200 : '200 OK',
    400 : '400 Bad Request',
    401 : '401 Unauthorized',
    403 : '403 Forbidden',
    404 : '404 Not Found',
    414 : '414 URI Too Long',
    500 : '500 Internal Server Error',
    501 : '501 Not Implemented',
}

class HTTPPlugin(BasePlugin):
    def __init__(self, socket, framework):
        BasePlugin.__init__(self, socket, framework)
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = ""

    def do_track(self):
        self.rfile = socket.SocketIO(self._skt, "r")
        self.wfile = socket.SocketIO(self._skt, "w")

        if not self.parse_message():
            self.finalize()
            return False

        if not self.handle_message():
            self.finalize()
            return False

        self.fix_headers()

        self.finalize()

        try:
            entry = {'test_http': {'METHOD' : self.method,
                               'PATH' : self.path,
                               'HEADERS' : self.headers,
                               'BODY' : self.body}}

            self.do_save(entry)
        except:
            return False

        return True

    def finalize(self):
        try:
            self.rfile.close()
        except:
            pass

        try:
            self.wfile.close()
        except:
            pass

        self._skt = None

    def parse_message(self):
        if (not self.read_request()):
            return False

        if (not self.read_headers()):
            return False

        if (not self.read_body()):
            return False

        return True

    def read_request(self):
        try:
            request_line = self.rfile.readline(2049)
        except socket.timeout:
            return False

        if (len(request_line) > 2048):
            self.reply(414)
            return False

        if (len(request_line) == 0):
            self.reply(400)
            return False

        request_line = request_line.split()

        self.method = str(request_line[0], 'utf-8')

        if self.method not in METHODS:
            # method is not an http method 400 error
            return False

        self.path = str(request_line[1], 'utf-8')
        self.path = urllib.parse.unquote(self.path)
        self.path = self.path.lower()

        if self.path[0] != '/':
            # path is not a path 400 error
            return False

        if (len(request_line) == 3):
            self.version = str(request_line[2], 'utf-8')

        return True

    def read_headers(self):
        while (True):
            try:
                line = self.rfile.readline(2049)
            except socket.timeout:
                return False

            if (len(line) > 2048):
                self.reply(400)
                return False

            if line in (b'\r\n', b'\n', b''):
                break

            line = str(line, 'utf-8')

            line = line.split(': ', 1)

            if (len(line) < 2):
                # bad header 400 error
                return False

            line[1] = line[1].rstrip('\n')
            line[1] = line[1].rstrip('\r\n')
            self.headers[line[0].lower()] = line[1]

        return True

    def read_body(self):
        if 'content-length' in self.headers:
            size = self.headers['content-length']

            try:
                size = int(size)
            except ValueError:
                return True

            try:
                self.body = str(self.rfile.read(size), 'utf-8')
            except TypeError:
                pass
            except socket.timeout:
                pass
        else:
            return True

        return True

    def handle_message(self):
        if not getattr(self, 'do_' + self.method)():
            return False

        return True

    def do_GET(self):
        if self.path == '/':
            self.reply(200, PAGE_LOGIN)
        elif self.path == '/login':
            self.reply(403)
        else:
            self.reply(404)

        return True

    def do_HEAD(self):
        if self.path == '/':
            self.reply(200, PAGE_LOGIN)
        elif self.path == '/login':
            self.reply(403)
        else:
            self.reply(404)

        return True

    def do_POST(self):
        if (self.path == '/'):
            self.reply(200, PAGE_LOGIN)
        elif (self.path == '/login'):
            self.reply(500)
        else:
            self.reply(404)

        return True

    def do_PUT(self):
        self.reply(501)

        return True

    def do_DELETE(self):
        self.reply(501)

        return True

    def do_TRACE(self):
        self.reply(501)

        return True

    def do_CONNECT(self):
        self.reply(501)

        return True

    def reply(self, code, body=None):
        self.send_reply(code)
        self.send_header(b'Date', bytes(self.date_string(), 'utf-8'))
        self.send_header(b'Content-Type', b'text/html')

        if body == None:
            body = PAGE_ERROR % {'error' : STATUS_CODES[code]}
            body = bytes(body, 'utf-8')

        self.send_header(b'Content-Length', str(len(body)).encode())
        self.send_header(b'Content', b'Closed')

        self.end_headers()

        self.wfile.write(body)

    def send_reply(self, code):
        self.wfile.write(b'HTTP/1.1 ')
        self.wfile.write(bytes(STATUS_CODES[code], 'utf-8'))
        self.wfile.write(b'\r\n')

    def send_header(self, type, content):
        self.wfile.write(type)
        self.wfile.write(b': ')
        self.wfile.write(content)
        self.wfile.write(b'\r\n')

    def end_headers(self):
        self.wfile.write(b'\r\n')

    def fix_headers(self):
        fixed_header = ""
        for header in self.headers:
            fixed_header += header
            fixed_header += ': '
            fixed_header += self.headers[header]
            fixed_header += '\r\n'

        self.headers = fixed_header

    def date_string(self):
        year, mon, mday, hour, min, sec, wday, yday, isdst = time.gmtime(time.time())
        return "%s, %02d %3s %4d %02d:%02d:%02d GMT" \
            % (DAYS[wday], mday, MONTHS[mon-1], year, hour, min, sec)