import unittest
import socket

from plugins.http import HTTPPlugin


def setup_test_config(test_port, test_module, test_class):
    return {
        'port': test_port,
        'module': test_module,
        'moduleClass': test_class,
        'table': 'test',
        'enabled': 'Yes',
        'rawSocket': 'No',
        'tableColumns': [[1, 'command', 'TEXT'], [2, 'path', 'TEXT'], [3, 'headers', 'TEXT'], [4, 'body', 'TEXT']]
    }


def setup_test_sockets(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('', port))
    server_socket.listen(1)
    test_socket_send = socket.socket()
    test_socket_send.connect(('', port))
    (test_socket_recv, addr) = server_socket.accept()
    server_socket.close()

    return test_socket_send, test_socket_recv


class HTTPPluginTest(unittest.TestCase):
    def test_go(self):
        pass

    def test_head(self):
        pass

    def test_post(self):
        pass

    def test_real_501(self):
        """
        Test a PUT command
        PUT, OPTIONS, DELETE, TRACE, and CONNECT should all have the same behavior.
        These commands send back a 501 error stating that the commands
        are not supported.
        """

        test_client, test_server = setup_test_sockets(8083)

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        test_client.send(b'PUT / HTTP/1.1\r\n'
                         b'Connection: close\r\n'
                         b'\r\n')

        plugin_test.handle_one_request()
        plugin_test.format_data()
        entry = plugin_test.get_entry()

        self.assertEqual(entry, {'test':
                                 {'command': 'PUT',
                                  'path': '/',
                                  'headers': 'Connection: close\n\n',
                                  'body': ''}})

        plugin_test.shutdown()
        test_client.close()

    def test_fake_501(self):
        """
        Test a bad http command
        If a command comes through that has no do_<command>
        defined it should be treated like a 501 and still
        be written to the database
        """

        test_client, test_server = setup_test_sockets(8083)

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        test_client.send(b'TEST / HTTP/1.1\r\n'
                         b'Connection: close\r\n'
                         b'\r\n')

        plugin_test.handle_one_request()
        plugin_test.format_data()
        entry = plugin_test.get_entry()

        self.assertEqual(entry, {'test':
                                 {'command': 'TEST',
                                  'path': '/',
                                  'headers': 'Connection: close\n\n',
                                  'body': ''}})

        plugin_test.shutdown()
        test_client.close()

if __name__ == '__main__':
    unittest.main()