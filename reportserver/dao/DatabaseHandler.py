__author__ = 'Charlie Mitchell <belmontrevenge@gmail.com>'
'''
This class will take in a request from the webserver, query the Sqlite database,
and return JSON.
'''

import os
import sqlite3

from common.GlobalConfig import Configuration
from reportserver.manager import dateTimeUtility

cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
global_config = Configuration(cfg_path).getInstance()
db_path = global_config.get_db_dir() + '/honeyDB.sqlite'

# Connect to given database.
# Defaults to the honeypot db, but another path can be passed in (mainly for testing).
# Database needs to exist first.
def connect(database_name=db_path):
    if not os.path.exists(database_name):
        print("Database does not exist in path: " + database_name)
        return None
    try:
        conn = sqlite3.connect(database_name)
    except sqlite3.OperationalError:
        print("Error connecting to database at: " + database_name)
    else:
        return conn

# Query DB and return JSON
# setting DB to TestDB created from DatabaseHandlerTest.py
def query_db(query, args=(), one=False):
    cur = connect().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
            for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

# Unit of Measure could be "weeks", "days", "hours", etc.
# Return all data from the DB within that measure of time as JSON.
def get_json_by_time(portnumber, unit, unit_size):
    begin_date = dateTimeUtility.get_begin_date(unit, unit_size)
    begin_date_iso = dateTimeUtility.get_iso_format(begin_date)
    tableName = global_config.get_plugin_config(portnumber)['table']
    date_time_field = global_config.get_db_datetime_name()

    #  query = query_db("SELECT * FROM %s where (datetime > '%s')" % (tableName, query_date_iso))
    queryString = "SELECT * FROM %s where (%s > '%s')" % (tableName, date_time_field, begin_date_iso)
    # print("queryString is: " + queryString)
    results = query_db(queryString)
    # print("results: " + results)

    return results

