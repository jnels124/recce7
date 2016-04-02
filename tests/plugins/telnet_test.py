import unittest.mock
from unittest.mock import patch
from unittest.mock import MagicMock

config_path = 'tests/framework/testConfig.cfg'


def make_mock_config(port, module, clsname):
    return dict(port=port, module=module, moduleClass=clsname, table='test', enabled='Yes', rawSocket='No',
                tableColumns=[[1, 'User_Name', 'TEXT'], [2, 'Password', 'TEXT'], [3, 'User_Data', 'TEXT']])


class TelnetTest(unittest.TestCase):
    def setUp(self):
        pass

