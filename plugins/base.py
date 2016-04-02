import platform
import socket
from threading import Thread

import datetime


class BasePlugin(Thread):
    def __init__(self, base_socket, framework):
        Thread.__init__(self)
        self._skt = base_socket
        self._framework = framework
        self._localAddress = base_socket.getsockname()[0]
        self._peerAddress = base_socket.getpeername()[0]
        self.kill_plugin = False

    def run(self):
        while self._skt and not self.kill_plugin:
            try:
                self.do_track()
            except ConnectionResetError as cre:
                error_number = cre.errno
                if error_number == 54:  # ERRNO 54 is 'connection reset by peer'
                    # Log that it is possible we are being scanned, would want to write this to the db
                    print("Maybe we are being scanned")
                    pass

        self._framework.plugin_stopped(self)

    def do_save(self, data):
        data_malformed = False
        #Add default values for all plugins
        keys = list(data.keys())
        # Should only be one key for the table name in the outer dictionary
        if len(keys) == 1:
            data_values_list = list(data.values())
            # Should only be one (inner) dictionary for the key
            if len(data_values_list) == 1:
                data_values = data_values_list[0]
                data_values['peerAddress'] = self._peerAddress
                data_values['localAddress'] = self._localAddress
                data_values['eventDateTime'] = datetime.datetime.now().isoformat()
                self._framework.insert_data({keys[0]:data_values})
            else:
                data_malformed = True
                pass
        else:
            data_malformed = True
            pass

        if data_malformed:
            print("Data to be inserted from plugin is malformed: " + self.name)
            #TODO log here
            self.shutdown()

    def shutdown(self):
        self.kill_plugin = True

        if self._skt:
            old_skt = self._skt
            self._skt = None
            if platform.system() == 'Linux':
                old_skt.shutdown(socket.SHUT_RDWR)
                old_skt.detach()
            old_skt.close()
        else:
            print("Socket already closed for plugin thread name: " + self.name)

        self.join()