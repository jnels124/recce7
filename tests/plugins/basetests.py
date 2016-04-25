import unittest
import socket
import os

from plugins.http import HTTPPlugin
from common.GlobalConfig import Configuration
from framework.frmwork import Framework
from framework.frmwork import main


def setup_test_config(test_port, test_module, test_class):
    return {
        'port': test_port,
        'module': test_module,
        'moduleClass': test_class,
        'table': 'test',
        'enabled': 'Yes',
        'rawSocket': 'No',
        'tableColumns': [[1,'command','TEXT'], [2,'path','TEXT'], [3, 'headers', 'TEXT'], [4, 'body', 'TEXT']]
    }


def setup_test_sockets():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server_socket.bind(('', 8083))
    server_socket.listen(1)
    test_socket_send = socket.socket()
    test_socket_send.connect(('', 8083))
    (test_socket_recv, addr) = server_socket.accept()
    server_socket.close()

    return test_socket_send, test_socket_recv


class BasePluginTest(unittest.TestCase):
    # Test the dictionary creation from get_entry inside the Base_Plugin
    def test_get_entry(self):
        # Try a PUT
        test_client,test_server = setup_test_sockets()

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        self.assertEqual(plugin_test.get_entry(),
            {'test' : {'command' : '', 'path' : '', 'headers' : '', 'body' : '',}})

        test_server.close()
        test_client.close()

    def test_get_plugin_port(self):
        test_client,test_server = setup_test_sockets()

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        self.assertEqual(plugin_test.get_plugin_port(), 8083)

        test_server.close()
        test_client.close()

    def test_get_table_name(self):
        test_client,test_server = setup_test_sockets()

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        self.assertEqual(plugin_test.get_table_name(), 'test')

        test_server.close()
        test_client.close()

    def test_get_table_columns(self):
        test_client,test_server = setup_test_sockets()

        plugin_test = HTTPPlugin(test_server, setup_test_config(8083, 'http', 'HTTPPlugin'), None)

        self.assertEqual(plugin_test.get_table_columns(), ['command','path','headers','body'])

        test_server.close()
        test_client.close()

if __name__ == '__main__':
    unittest.main()