from database import DB_Init
from common.GlobalConfig import GlobalConfig
from common.GlobalConfig import Configuration
import unittest
from unittest.mock import patch
import os


class DB_Init_test(unittest.TestCase):

    testpath_exist = os.getcwd() + '/tests/database/DB_Init_testDir'
    testpath_non_exist = os.getcwd() + '/tests/database/DB_Init_testDirDoesNotExist'
    testpath_with_db = os.getcwd() + '/tests/database/DB_Init_testDirDB/honeyDB'
    testpath_mod_db = os.getcwd() + '/tests/database/DB_Init_testModDirDB/honeyDB'


    @patch('os.mkdir')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_exist)
    def test_create_db_dir_exists(self, gci_get_db_dir, os_mkdir):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        DB_Init.create_db_dir(gci)
        self.assertFalse(os_mkdir.called)


    @patch('os.mkdir')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_non_exist)
    def test_create_db_dir_non_exist(self, gci_get_db_dir, os_mkdir):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        DB_Init.create_db_dir(gci)
        self.assertTrue(os_mkdir.called)


    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_create_db_database_exists(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        DB_Init.create_db(gci)
        self.assertFalse(sqlite3_connect.called)


    @patch('sqlite3.connect')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_exist)
    def test_create_db_database_non_exist(self, gci_get_db_dir, sqlite3_connect):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        DB_Init.create_db(gci)
        self.assertTrue(sqlite3_connect.called)


    def test_table_list_diff(self):
        table_list = ['table1', 'table2', 'table3']
        table_list_match = ['table2', 'table3', 'table1']
        table_list_non_match = ['table2', 'table3', 'table4']
        self.assertTrue(DB_Init.table_list_diff(table_list, table_list_non_match) == ['table4'])
        self.assertTrue(DB_Init.table_list_diff(table_list, table_list_match) == [])


    def test_get_config_table_list(self):
        expected_tables = ['test_http_test', 'test_http2_test', 'test_telnet_test']
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        self.assertEqual(expected_tables, DB_Init.get_config_table_list(gci.get_ports(), gci.get_plugin_dictionary()))


    @patch('database.Table_Init.create_table')
    def test_create_non_exist_tables_diff(self, Table_Init_mod):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        table_diff = ['test4']
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertTrue(Table_Init_mod.called)


    @patch('database.Table_Init.create_table')
    def test_count_create_non_exist_tables(self, Table_Init_mod):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        table_diff = ['test4', 'test5', 'test6']
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertEqual(3, Table_Init_mod.call_count)


    @patch('database.Table_Init.create_table')
    def test_create_non_exist_tables(self, Table_Init_mod):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        table_diff = []
        DB_Init.create_non_exist_tables(table_diff, gci)
        self.assertFalse(Table_Init_mod.called)


    def test_create_dict_config_column_good(self):
        expected_column_list = {'test_telnet_test': [[1, 'user_data_telnet', 'TEXT'], [2, 'user_data_telnet2', 'TEXT']],
                                'test_http_test': [[1, 'user_data', 'TEXT']],
                                'test_http2_test': [[1, 'user_data2', 'TEXT']]}
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        self.assertTrue(expected_column_list == DB_Init.create_dict_config_column_list(gci))


    def test_create_dict_config_column_bad(self):
        wrong_column_list = {'test_telnet_test_wrong': [[1, 'Test_col', 'TEXT'], [2, 'User_Data', 'TEXT']],
                                'test_http2_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']],
                                'test_http_test': [[1, 'someNumber', 'INTEGER'], [2, 'someText', 'TEXT']]}
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        self.assertFalse(wrong_column_list == DB_Init.create_dict_config_column_list(gci))

    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_create_dict_schema_column_list(self,gci_get_db_dir):
        expected_column_list = {'test_http_test': [(0, 'ID', 'INTEGER', 1, None, 1),
                                                   (1, 'eventDateTime', 'TEXT', 0, None, 0),
                                                   (2, 'peerAddress', 'TEXT', 0, None, 0),
                                                   (3, 'localAddress', 'TEXT', 0, None, 0),
                                                   (4, 'user_data', 'TEXT', 0, None, 0)],
                                'test_http2_test': [(0, 'ID', 'INTEGER', 1, None, 1),
                                                    (1, 'eventDateTime', 'TEXT', 0, None, 0),
                                                    (2, 'peerAddress', 'TEXT', 0, None, 0),
                                                    (3, 'localAddress', 'TEXT', 0, None, 0),
                                                    (4, 'user_data2', 'TEXT', 0, None, 0)],
                                'test_telnet_test': [(0, 'ID', 'INTEGER', 1, None, 1),
                                                     (1, 'eventDateTime', 'TEXT', 0, None, 0),
                                                     (2, 'peerAddress', 'TEXT', 0, None, 0),
                                                     (3, 'localAddress', 'TEXT', 0, None, 0),
                                                     (4, 'user_data_telnet', 'TEXT', 0, None, 0),
                                                     (5, 'user_data_telnet2', 'TEXT', 0, None, 0)]}
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        self.assertTrue(expected_column_list == DB_Init.create_dict_schema_column_list(gci))

    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_create_dict_transformed_column_list(self,gci_get_db_dir):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg',True).getInstance()
        expected_column_dict = {'test_http2_test': [[4, 'user_data2', 'TEXT']],
                                'test_telnet_test': [[4, 'user_data_telnet', 'TEXT'], [5, 'user_data_telnet2', 'TEXT']],
                                'test_http_test': [[4, 'user_data', 'TEXT']]}
        self.assertTrue(expected_column_dict ==
                       (DB_Init.create_dict_transformed_column_list(DB_Init.create_dict_schema_column_list(gci))))

    #TODO create a test for updating structure need to figure out how to change config
    #files in the middle of test

    @patch('database.Table_Init.change_table_structure')
    @patch.object(GlobalConfig, 'get_db_dir', return_value=testpath_with_db)
    def test_update_table_structure(self,gci_get_db_dir,change_table_structure):
        gci = Configuration('tests/database/test_configs/DB_Init_test.cfg', True).getInstance()
        DB_Init.update_table_structure(gci)
        self.assertFalse(change_table_structure.called)
        gci = Configuration('tests/database/test_configs/DB_Init_testMod.cfg', True).getInstance()
        DB_Init.update_table_structure(gci)
        self.assertTrue(change_table_structure.called)













