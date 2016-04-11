import grp
import os
import pwd
import signal

from importlib import import_module
from common.GlobalConfig import Configuration
from database.DataManager import DataManager
from framework.networklistener import NetworkListener

__author__ = 'Jesse Nelson <jnels1242012@gmail.com>, ' \
             'Randy Sorensen <sorensra@msudenver.edu>'

default_cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'


class Framework:
    def __init__(self, cfg_path):
        self.global_config = Configuration(cfg_path).getInstance()
        self.plugin_imports = {}
        self.listener_list = {}
        self.running_plugins_list = []
        self.data_manager = None
        self.shutting_down = False

    def start(self):
        print('RECCE7 starting (pid ' + str(os.getpid()) + ')')
        print('Press Ctrl+C to exit.\n')
        self.set_shutdown_hook()
        if not self.drop_permissions():
            return
        self.data_manager = DataManager(self.global_config)
        self.data_manager.start()
        self.start_listeners()

    @staticmethod
    def drop_permissions():
        if os.getuid() != 0:
            return True

        dist_name = os.getenv('RECCE7_OS_DIST')
        users_dict = {'centos': ('nobody', 'nobody'),
                      'debian': ('nobody', 'nogroup')}
        if dist_name not in users_dict:
            print(
                'Unable to lower permission level - not continuing as\n'
                'superuser. Please set the environment variable\n'
                'RECCE7_OS_DIST to one of:\n\tcentos\n\tdebian\n'
                'or rerun as a non-superuser.')
            return False
        lowperm_user = users_dict[dist_name]
        nobody_uid = pwd.getpwnam(lowperm_user[0]).pw_uid
        nogroup_gid = grp.getgrnam(lowperm_user[1]).gr_gid

        os.setgroups([])
        os.setgid(nogroup_gid)
        os.setuid(nobody_uid)
        os.umask(0o077)

        return True

    def create_import_entry(self, port, name, clsname):
        imp = import_module('plugins.' + name)
        self.plugin_imports[port] = getattr(imp, clsname)

    def start_listeners(self):
        ports = self.global_config.get_ports()
        for port in ports:
            print('Listener started on port: ' + str(port))
            plugin_config = self.global_config.get_plugin_config(port)
            module = plugin_config['module']
            clsname = plugin_config['moduleClass']
            self.create_import_entry(port, module, clsname)
            listener = NetworkListener(plugin_config, self)
            listener.start()
            self.listener_list[port] = listener

    def set_shutdown_hook(self):
        signal.signal(signal.SIGINT, self.shutdown)

    def shutdown(self, *args):
        self.shutting_down = True

        print("Shutting down network listeners")
        for listener in self.listener_list.values():
            listener.shutdown()

        print("Shutting down plugins")
        for plugin in self.running_plugins_list:
            plugin.shutdown()

        print("Shutting down data manager")
        self.data_manager.shutdown()

        print("Goodbye.")

    #
    # Framework API
    #

    '''
    Returns the configuration dictionary for the plugin
    running on the specified port.

    :param port: a port number associated with a loaded plugin
    :return: a plugin configuration dictionary
    '''
    def get_config(self, port):
        return self.global_config.get_plugin_config(port)

    '''
    Spawns the plugin configured by 'config' with the provided
    (accepted) socket.

    :param socket: an open, accepted socket returned by
                   socket.accept()
    :param config: the plugin configuration dictionary describing
                   the plugin to spawn
    :return: a reference to the plugin that was spawned
    '''
    def spawn(self, socket, config):
        # ToDo Throw exception if plugin class not found
        plugin_class = self.plugin_imports[config['port']]
        plugin = plugin_class(socket, config, self)
        plugin.start()
        self.running_plugins_list.append(plugin)
        return plugin

    '''
    Inserts the provided data into the data queue so that it can
    be pushed to the database.

    :param data: data object to add to the database
    '''
    def insert_data(self, data):
        self.data_manager.insert_data(data)

    '''
    Tells the framework that the specified plugin has stopped
    running and doesn't need to be shutdown explicitly on program
    exit.

    :param plugin: a reference to a plugin
    '''
    def plugin_stopped(self, plugin):
        if self.shutting_down:
            return

        self.running_plugins_list.remove(plugin)


def main(cfg_path=None):
    framework = Framework(default_cfg_path)
    framework.start()

if __name__ == '__main__': main()
