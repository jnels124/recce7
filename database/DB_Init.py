import os
import sqlite3
from database import Table_Init
from database.DataValidation import DataValidation

__author__ = 'Ben Phillips'
'''use to create a folder and sqlite data file in the users home directory'''

'''calls methods needed to create the database'''
def create_default_database(global_config_instance):

    create_db_dir(global_config_instance)
    create_db(global_config_instance)
    update_schema(global_config_instance)

'''creates the database directory if it does not exist'''
def create_db_dir(global_config_instance):
    """if database directory does not exist create it"""
    if not os.path.isdir(global_config_instance.get_db_dir()):
        print("Database Directory not found, creating database directory...")
        os.mkdir(global_config_instance.get_db_dir())

'''creates the database if it does not exist'''
def create_db(global_config_instance):
    '''if database file does not exist in directory create it'''
    if not os.path.exists(global_config_instance.get_db_dir() + '/honeyDB.sqlite'):
        print("Database File not found, creating database file...")
        connection = sqlite3.connect(global_config_instance.get_db_dir() + '/honeyDB.sqlite')
        connection.close()

'''calls the appropriate methods to update the database tables with changes to columns'''
def update_schema(global_config_instance):
    '''now the database is guaranteed to exist, we must find out if the
    schema is correct and create the appropriate tables I am creating
    another validation object for this purpose and am also storing the
    schema and port list locally so that it is easy to do this'''

    '''holds the list of tables defined in the configuration'''
    '''if the distinct sets of tables are not equal'''
    '''create database tables that do not exist'''
    create_non_exist_tables(table_list_diff(DataValidation(global_config_instance).get_tables(),
                                            get_config_table_list(global_config_instance.get_ports(),
                                                                  global_config_instance.get_plugin_dictionary())),
                            global_config_instance)
    '''now that the tables do exist lets update the information from the database'''
    DataValidation(global_config_instance).update_tables_and_schema(global_config_instance)
    '''now our tables exist with a primary key sequence of ID'''
    '''now i must check each table and add columns'''
    '''create a dictionary of config column lists'''
    '''create a dictionary of database column lists'''
    #this call may not do anything at all anymore
    #update_schema_column_list(global_config_instance)
    '''transform database column list this contains the column definitions in
       the same way as the config does'''
    update_table_structure(global_config_instance)



'''returns the table list from the configuration singleton that correspond to ports provided'''
def get_config_table_list(port_list, schema_dict):

    config_table_list = []
    for port in port_list:
        config = schema_dict.get(port)
        config_table_list.append(config.get('table'))
    return config_table_list


'''return list of tables that are different between the current database table list and the config's table list'''
def table_list_diff(current_database_table_list,config_table_list):
    if not set(current_database_table_list) == set(config_table_list):
        '''return the left hand difference between the schema and config table sets'''
        return list(set(config_table_list) - set(current_database_table_list))
    else:
        return []


#create tables that do not exist from the table difference between the current database and the configuration
def create_non_exist_tables(table_diff,global_config_instance):
    if len(table_diff) > 0:
        for table in table_diff:
            Table_Init.create_table(table, global_config_instance)
        print('Updated database schema, table names now match configuration.')
    else:
        print('Database Schema and Configuration table names already match.')

'''get a dictionary of tables and corresponding columns from the config'''
def create_dict_config_column_list(global_config_instance):
    config_column_lists = {}
    for port in global_config_instance.get_ports():
        value = global_config_instance.get_plugin_dictionary().get(port)
        config_column_lists[value.get('table')] = value.get('tableColumns')
    return config_column_lists

'''get a dictionary of tables and corresponding columns from the existing database'''
def create_dict_schema_column_list(global_config_instance):
    database_column_lists = {}
    database_schema = DataValidation(global_config_instance).get_schema()
    for schema in database_schema:
        database_column_lists[schema] = database_schema.get(schema)
    return database_column_lists

'''returns only custom plugin defined columns from database schema i.e. ignores default columns'''
def create_dict_transformed_column_list(database_column_lists):
    transformed_db_column_list = {}
    for table in database_column_lists:
        col_list = database_column_lists.get(table)
        for column in col_list:
            transformed_db_column_list[table] = []
        '''default column ids to ignore'''
        default_list = []
        for default in Table_Init.default_columns:
            default_list.append(default[0])
        for column in col_list:
            '''ignores the default columns'''
            if column[1] in default_list:
                continue
            transformed_db_column_list[table].append([column[0],column[1],column[2]])
    return transformed_db_column_list

#this code may not do anything at all anymore
'''def update_schema_column_list(global_config_instance):
    for schema in DataValidation(global_config_instance).get_schema():
        create_dict_schema_column_list(global_config_instance)[schema] = \
                                       DataValidation(global_config_instance).get_schema().get(schema)'''



def update_table_structure(global_config_instance):
    for table in create_dict_config_column_list(global_config_instance):
            if not [(x[1],x[2]) for x in create_dict_config_column_list(global_config_instance).get(table)] == \
                   [(x[1],x[2]) for x in create_dict_transformed_column_list(create_dict_schema_column_list(global_config_instance)).get(table)]:
                Table_Init.change_table_structure(table,
                                                  create_dict_config_column_list(global_config_instance).get(table),
                                                  create_dict_schema_column_list(global_config_instance).get(table),
                                                  global_config_instance)