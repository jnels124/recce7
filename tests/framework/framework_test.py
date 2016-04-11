import grp
import os
import pwd
import socket
import unittest
import unittest.mock
from database.DataManager import DataManager
from framework.frmwork import Framework
from framework.frmwork import main
from framework.networklistener import NetworkListener
from plugins.base import BasePlugin
from plugins.http import HTTPPlugin
from unittest.mock import patch
from unittest.mock import MagicMock
import os

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

config_path = 'tests/framework/testConfig.cfg'


def make_mock_config(port, module, clsname):
    return {
        'port': port,
        'module': module,
        'moduleClass': clsname,
        'table': 'test',
        'enabled': 'Yes',
        'rawSocket': 'No',
        'tableColumns': [[1,'someNumber','INTEGER'], [2,'someText','TEXT']]
    }


class FrameworkTest(unittest.TestCase):
    def setUp(self):
       pass


    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_plugins_enabled(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        expected = {
            8082: make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        }
        self.assertEqual(expected, framework.global_config.get_plugin_dictionary())
        self.assertEqual(1, mock_nl_start.call_count)
        self.assertTrue(mock_dm_start.called)

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_plugins_disabled(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        self.assertTrue(8083 not in framework.global_config.get_plugin_dictionary())
        self.assertTrue(8082 in framework.global_config.get_plugin_dictionary())
        self.assertEqual(1, mock_nl_start.call_count)

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    def test_get_config(self, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        expected = make_mock_config(8082, 'HTTPPlugin', 'HTTPPlugin')
        self.assertEqual(expected, framework.get_config(8082))

    @patch('database.DataManager.DataManager.start')
    @patch('framework.networklistener.NetworkListener.start')
    @patch.object(socket.socket, 'getsockname', return_value='0.0.0.0')
    @patch.object(socket.socket, 'getpeername', return_value='0.0.0.1')
    def test_spawn(self, mock_gpn, mock_gsn, mock_nl_start, mock_dm_start):
        framework = Framework(config_path)
        framework.start()
        with patch('plugins.HTTPPlugin.HTTPPlugin.start') as mock_http_start:
            framework.spawn(socket.socket(), {'port': 8082})
        self.assertTrue(mock_http_start.called)

    @patch.object(Framework, 'start')
    def test_main(self, mock_framework_start):
        main()
        self.assertTrue(mock_framework_start.called)

    def test_get_db_dir(self):
        fw = Framework(config_path)
        self.assertEqual(fw.global_config.get_db_dir(),
                         os.getenv('HOME') + '/honeyDB')

    @patch('os.getuid', return_value = 0)
    @patch('os.setgroups')
    @patch('os.setuid')
    @patch('os.setgid')
    @patch('os.getenv', return_value='debian')
    def test_drop_permissions(self, mock_getenv, mock_setgid, mock_setuid,
                              mock_setgroups, mock_getuid):
        fw = Framework(config_path)

        nobody_uid = pwd.getpwnam('nobody').pw_uid
        nogroup_gid = grp.getgrnam('nogroup').gr_gid

        fw.drop_permissions()

        mock_setuid.assert_called_with(nobody_uid)
        mock_setgid.assert_called_with(nogroup_gid)
        mock_setgroups.assert_called_with([])

    @patch('os.setgroups')
    @patch('os.setuid')
    @patch('os.setgid')
    def test_dont_drop_permissions(self, mock_setgid, mock_setuid,
                                   mock_setgroups):
        fw = Framework(config_path)
        fw.drop_permissions()

        self.assertFalse(mock_setuid.called)
        self.assertFalse(mock_setgid.called)
        self.assertFalse(mock_setgroups.called)

    @patch('os.getuid', return_value = 0)
    @patch('os.setgroups')
    @patch('os.setuid')
    @patch('os.setgid')
    @patch('os.getenv', return_value='multics')
    def test_cant_drop_permissions(self, mock_getenv, mock_setgid, mock_setuid,
                                   mock_setgroups, mock_getuid):
        fw = Framework(config_path)
        self.assertFalse(fw.drop_permissions())

    @patch('database.DataManager.DataManager.start', return_value=None)
    @patch('framework.networklistener.NetworkListener.start')
    def test_insert_data(self, mock_nl_start, mock_dm_start):
        fw = Framework(config_path)
        fw.start()
        test_dict = {'a': 1, 'b': 2}
        with patch('database.DataManager.DataManager.insert_data') as mock_insert_data:
            fw.insert_data(test_dict)
            mock_insert_data.assert_called_with(test_dict)

    def test_shutdown(self):
        fw = Framework(config_path)
        for i in range(5):
            fw.listener_list[i] = MagicMock()
            fw.listener_list[i].shutdown = MagicMock()
        for i in range(5):
            fw.running_plugins_list.append(MagicMock())
            fw.running_plugins_list[i].shutdown = MagicMock()
        fw.data_manager = MagicMock()
        fw.data_manager.shutdown = MagicMock()

        fw.shutdown(None)

        for listener in fw.listener_list.values():
            self.assertTrue(listener.shutdown.called)
        for plugin in fw.running_plugins_list:
            self.assertTrue(plugin.shutdown.called)
        self.assertTrue(fw.data_manager.shutdown.called)

    def test_plugin_stopped(self):
        fw = Framework(config_path)
        for i in range(5):
            fw.running_plugins_list.append(MagicMock())
        stopped_plugin = fw.running_plugins_list[1]
        fw.plugin_stopped(stopped_plugin)
        self.assertFalse(stopped_plugin in fw.running_plugins_list)

        stopped_plugin = fw.running_plugins_list[2]
        fw.shutting_down = True
        fw.plugin_stopped(stopped_plugin)
        self.assertTrue(stopped_plugin in fw.running_plugins_list)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
