import unittest
import sqlite3
import os
import datetime

from common.GlobalConfig import Configuration
from reportserver.dao import DatabaseHandler

class DatabaseHandlerTest(unittest.TestCase):

    # Creates a test DB with 1 table and 1000 entries with different timestamps.
    def setUp(self):
        conn = sqlite3.connect("TestDB.sqlite")
        c = conn.cursor()
        c.execute('''CREATE TABLE Dates (col1 text, col2 text, eventDateTime text)''')
        test_start_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)

        for x in range(0, 1000):
            d = datetime.timedelta(weeks=x)
            insert_date = (test_start_date + d)
            insert_date_iso = insert_date.isoformat()
            c.execute("INSERT INTO Dates VALUES ('TEXT1','TEXT2','%s')" % insert_date_iso)

        conn.commit()

    # Tests connecting to the DB. Includes testing for incorrect paths.
    def test_connect(self):
        # Negative testing
        self.assertIsNone(DatabaseHandler.connect("database"))
        self.assertIsNone(DatabaseHandler.connect("database.db"))
        self.assertIsNone(DatabaseHandler.connect("asdl;kfjeiei"))
        self.assertIsNone(DatabaseHandler.connect("./honeyDB/honeyDB.sqllite"))
        self.assertIsNone(DatabaseHandler.connect("./honeyDB/honeyDB.db"))
        self.assertIsNone(DatabaseHandler.connect(" "))
        self.assertIsNone(DatabaseHandler.connect(""))

        # Testing for correct DB (Database must exist first for this test to pass)
        cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
        global_config = Configuration(cfg_path).getInstance()
        db_path = global_config.get_db_dir() + '/honeyDB.sqlite'
        conn = sqlite3.connect(db_path)
        self.assertEquals(DatabaseHandler.connect(db_path), conn)

        # Test default
        self.assertEquals(DatabaseHandler.connect(), conn)

    # TODO - MORE TESTS!!!
    def test_query_db(self):
        json_query = DatabaseHandler.query_db("SELECT * FROM Castlevania where (system = 'NES')")
        expected = [
            {'title': 'Castlevania', 'system': 'NES', 'datetime': '1987-05-01T00:00:00'},
            {'title': 'Castlevania II: Simons Quest', 'system': 'NES', 'datetime': '1988-12-01T00:00:00'},
            {'title': 'Castlevania III: Draculas Curse', 'system': 'NES', 'datetime': '1990-09-01T00:00:00'}
        ]
        self.assertEqual(json_query, expected)

        json_query = DatabaseHandler.query_db("SELECT * FROM Zelda where (year <= '1993')")
        expected = [
            {'system': 'NES', 'title': 'The Legend of Zelda', 'year': '1987'},
            {'system': 'NES', 'title': 'Zelda II: The Adventure of Link', 'year': '1988'},
            {'system': 'SNES', 'title': 'The Legend of Zelda: A Link to the Past', 'year': '1992'},
            {'system': 'Game Boy', 'title': 'The Legend of Zelda: Links Awakening', 'year': '1993'}
        ]
        self.assertEqual(json_query, expected)

    # TODO - MORE TESTS!!!
    def test_get_json_by_time(self):
        query = DatabaseHandler.get_json_by_time("Dates", "weeks", 150)
        expected = [
            {"title": "Castlevania: Lords of Shadow 2", "datetime": "2014-02-25T00:00:00", "system": "PlayStation 3"},
            {"title": "Castlevania: Lords of Shadow 2", "datetime": "2014-02-25T00:00:00", "system": "Xbox 360"}
        ]
        self.assertEqual(query, expected)

    def test_get_table_name(self):
        self.assertEqual(DatabaseHandler.get_table_name(8082), "test_http")
        self.assertEqual(DatabaseHandler.get_table_name(8083), "test_http2")
        self.assertEqual(DatabaseHandler.get_table_name(8023), "test_telnet")

    def test_get_table_datetime_field(self):
        self.assertEqual(DatabaseHandler.get_table_datetime_field(8082), "eventDateTime")
        self.assertEqual(DatabaseHandler.get_table_datetime_field(8083), "eventDateTime")
        self.assertEqual(DatabaseHandler.get_table_datetime_field(8023), "eventDateTime")

    def tearDown(self):
        os.remove("TestDB.sqlite")

if __name__ == "__main__":
    unittest.main()