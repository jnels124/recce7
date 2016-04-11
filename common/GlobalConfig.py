import configparser
import os

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>' \
             'Dina Steeve<dsteeve@msudenver.edu>'

#default location unless a path is sent to us
default_cfg_path = 'config/plugins.cfg'

#todo:  currently can't override this one
default_global_cfg_file = 'config/global.cfg'


class Configuration(object):
    __instance = None


    #Refresh should only be set to True when testing, or you want to refresh the information.
    #This could be a threading issue if done in a multi-threaded environment!!  Be careful when setting Refresh=True
    def __new__(cls, path=None, refresh=False):
        ##print ('new on config was called.')
        if Configuration.__instance is None or refresh == True:
            Configuration.__instance = object.__new__(cls)
            config_location = path or default_cfg_path
            Configuration.__instance.val = Configuration.__instance.__read_config(config_location)

        return Configuration.__instance


    #Returns back an instance of the globalconfig class.
    def getInstance(self):
        return self.__instance.val


    # ToDo: Dont use eval!
    def __create_config_object(self, plugin, config_parser):
        port = int(config_parser.get(plugin, 'port'))
        table_name = config_parser.get(plugin, 'table')
        enabled = config_parser.get(plugin, 'enabled')
        column_defs = eval(config_parser.get(plugin, 'tableColumns'))
        module = config_parser.get(plugin, 'module')
        module_class = config_parser.get(plugin, 'moduleClass')
        raw_socket = config_parser.get(plugin, 'rawSocket')

        config_object = {
            'port': port,
            'table': table_name,
            'enabled': enabled,
            'tableColumns': column_defs,
            'module': module,
            'moduleClass': module_class,
            'rawSocket': raw_socket
        }

        return port, module, config_object

    def __read_config(self, cfg_path):
        #print("Reading the plugin config file: " + cfg_path)
        config_parser = configparser.ConfigParser()
        plugin_config_file = cfg_path

        config_parser.read(plugin_config_file)

        plugin_dictionary= {}
        enabled_ports = []

        plugins = config_parser.sections()
        for plugin in plugins:
            (port, module, config_object) = self.__create_config_object(plugin,config_parser)
            if config_object['enabled'].lower() == 'yes':
                plugin_dictionary[port] = config_object
                enabled_ports.append(port)

        # read in global config for reportserver and database sections
        config_parser.read(default_global_cfg_file)
        rserver_dictionary=config_parser['ReportServerSection']
        database_dictionary = config_parser['DatabaseSection']

        return GlobalConfig(plugin_dictionary, enabled_ports, rserver_dictionary, database_dictionary)


##The actual thing that holds the configuration data in the *.cfg file
class GlobalConfig:
    def __init__(self, plugin_dictionary, ports, rs_dictionary, database_dictionary):
        self.__plugin_dictionary = plugin_dictionary
        self.__enabled_ports = ports
        self.__rserver_dictionary = rs_dictionary
        self.__db_dictionary = database_dictionary

    #
    # Config API
    #



    def get_db_name(self):
        return self.__db_dictionary["database.name"]

    '''
    Returns a string indicating the location where the SQLite
    database file will be stored.

    :return: a string containing an absolute path
    '''
    def get_db_dir(self):
        db_dir = os.getenv('RECCE7_DB_PATH') or os.getenv('HOME') or '.'
        return db_dir + '/' + self.get_db_name()

    def get_db_datetime_name(self):
        return self.__db_dictionary["database.datetime.name"]

    def get_db_peerAddress_name(self):
        return self.__db_dictionary["database.peerAddress.name"]

    def get_db_localAddress_name(self):
        return self.__db_dictionary["database.localAddress.name"]

    '''
    Returns a list of ports with enabled plugins listening.

    :return: a list of integers representing TCP/IP ports
    '''
    def get_ports(self):
        return self.__enabled_ports.copy()

    '''
    Returns the configuration dictionary for the plugin listening
    on the specified port.

    :param port: an integer specifying a TCP/IP port
    :return: a dictionary with the config file parameters for the
             plugin that listens on port
    '''
    def get_plugin_config(self, port):
        return self.__plugin_dictionary[port]

    def get_plugin_dictionary(self):
        return self.__plugin_dictionary

    def get_report_server_host(self):
        return self.__rserver_dictionary["reportserver.host"]

    def get_report_server_port(self):
        port = self.__rserver_dictionary["reportserver.port"]
        return int(port)


