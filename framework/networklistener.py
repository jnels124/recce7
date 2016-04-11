import platform
import socket

from threading import Thread, Lock

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

HOST = ''


class NetworkListener(Thread):
    def __init__(self, config, framework):
        super().__init__()
        self.config = config
        self.port = config['port']
        self.framework = framework
        self.session_socket = None
        self.lock = Lock()
        self.running = False
        self.__connection_count = 0

    @property
    def connection_count(self):
        with self.lock:
            return self.__connection_count

    @connection_count.setter
    def connection_count(self, val):
        with self.lock:
            self.__connection_count = val

    # Override
    def run(self):
        self.running = True
        while self.running:
            self.session_socket = socket.socket(socket.AF_INET,
                                                socket.SOCK_STREAM)
            self.session_socket.setsockopt(socket.SOL_SOCKET,
                                           socket.SO_REUSEADDR, 1)
            self.session_socket.bind((HOST, self.port))
            self.session_socket.listen(1)
            self.start_listening(self.session_socket)
            self.session_socket.close()
            self.connection_count += 1
        print("Listener on port", self.port, "shutting down")
        self.session_socket = None

    def start_listening(self, local_socket):
        try:
            (new_socket, addr) = local_socket.accept()
            if self.running:
                print("New connection from", addr, "on port", self.port)
                self.framework.spawn(new_socket, self.config)
        except ConnectionAbortedError as e:
            if not self.running:
                return
            raise e
        except OSError as e:
            if e.errno == 22 and not self.running:
                return
            raise e
        except Exception as e:
            print("Error on connection: ", e)
            raise e

    def shutdown(self):
        self.running = False
        if self.session_socket:
            if platform.system() == 'Linux':
                self.session_socket.shutdown(socket.SHUT_RDWR)
            else:
                self.session_socket.close()
        self.join()
