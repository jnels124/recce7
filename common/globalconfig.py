import configparser

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>' \
             'Dina Steeve <dsteeve@msudenver.edu>'


class GlobalConfig:
    __instance = None

    class _GlobalConfig:
        def __init__(self, plugin_cfg_path, global_cfg_path):
            self._plugin_cfg_path = plugin_cfg_path
            self._plugin_cfg_dict = {}

            self._global_cfg_path = global_cfg_path
            self._global_cfg_dict = {}

            self._enabled_ports = []

        def create_plugin_dict(self, plugin, config_parser):
            config_object = dict(config_parser[plugin])
            #TODO: Don't use eval!
            config_object['port'] = int(config_object['port'])
            config_object['tableColumns'] = eval(config_object['tableColumns'])
            return config_object

        def read_plugin_config(self):
            if len(self._plugin_cfg_dict) != 0:
                return
            self._enabled_ports = []
            config_parser = configparser.RawConfigParser()
            config_parser.optionxform = lambda option: option
            config_parser.read(self._plugin_cfg_path)

            plugin_sections = config_parser.sections()
            for plugin in plugin_sections:
                config_object = self.create_plugin_dict(plugin, config_parser)
                port = int(config_object['port'])
                if config_object['enabled'].lower() == 'yes':
                    self._plugin_cfg_dict[port] = config_object
                    self._enabled_ports.append(port)

        def read_global_config(self):
            if len(self._global_cfg_dict) != 0:
                return
            config_parser = configparser.ConfigParser()
            config_parser.read(self._global_cfg_path)

            sections = config_parser.sections()
            for section in sections:
                self._global_cfg_dict[section] = config_parser[section]

        #
        # Config API
        #

        def get_plugin_dictionary(self):
            return self._plugin_cfg_dict

        def get_ports(self):
            """
            Returns a list of ports with enabled plugins listening.

            :return: a list of integers representing TCP/IP ports
            """
            return self._enabled_ports.copy()

        def get_plugin_config(self, port):
            """
            Returns the configuration dictionary for the plugin listening
            on the specified port.

            :param port: an integer specifying a TCP/IP port
            :return: a dictionary with the config file parameters for the
                     plugin that listens on port
            """
            return self._plugin_cfg_dict[port]

        def get_report_server_host(self):
            return self['ReportServer']['reportserver.host']

        def get_report_server_port(self):
            port = self['ReportServer']['reportserver.port']
            return int(port)

        def get_db_datetime_name(self):
            return self['Database']['datetime.name']

        def __getitem__(self, item):
            return self._global_cfg_dict[item]

    def __new__(cls, plugin_cfg_path=None, global_cfg_path=None, refresh=False):
        """
        Returns the configuration singleton, or instantiates it
        if: 1) no instance exists yet, or 2) the refresh parameter
        is True.

        :param plugin_cfg_path: A string containing the path to
                                the plugin configuration file.
        :param global_cfg_path: A string containing the path to
                                the global/program configuration
                                file.
        :param refresh: When True, any current instance will be replaced by a
                        new instance (useful for unit testing).
        :return: A GlobalConfig instance.
        """
        if refresh or not GlobalConfig.__instance:
            GlobalConfig.__instance = GlobalConfig._GlobalConfig(
                plugin_cfg_path, global_cfg_path)
            GlobalConfig.__instance._global_cfg = {}
            GlobalConfig.__instance._plugin_cfg = {}
            GlobalConfig.__instance._enabled_ports = []
        return GlobalConfig.__instance

    def __getattr__(self, name):
        return getattr(GlobalConfig.__instance, name)

    def __setattr__(self, name, value):
        return setattr(GlobalConfig.__instance, name, value)

    def __getitem__(self, item):
        return GlobalConfig.__instance[item]
