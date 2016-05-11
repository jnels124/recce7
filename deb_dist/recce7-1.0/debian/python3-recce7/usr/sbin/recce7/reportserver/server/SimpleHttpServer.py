import os
import time

from common.logger import Logger
from common.globalconfig import GlobalConfig
from http.server import HTTPServer

from reportserver.server.RESTRequestHandler import RestRequestHandler


#Create and start the HTTP Server


class SimpleHttpServer:
    def __init__(self):
        plugin_cfg_path = os.getenv('RECCE7_PLUGIN_CONFIG') or 'config/plugins.cfg'
        global_cfg_path = os.getenv('RECCE7_GLOBAL_CONFIG') or 'config/global.cfg'
        self.g_config = GlobalConfig(plugin_cfg_path, global_cfg_path)
        self.g_config.read_plugin_config()
        self.g_config.read_global_config()
        self.host = self.g_config.get_report_server_host()
        self.port = self.g_config.get_report_server_port()
        log_path = self.g_config['ReportServer']['reportserver.logName']
        log_level = self.g_config['ReportServer']['reportserver.logLevel']
        self.log = Logger(log_path, log_level).get('reportserver.server.SimpleHTTPServer.SimpleHTTPServer')

    def setupAndStart(self):

        server_address = (self.host, self.port)

        request_handler = RestRequestHandler

        # instantiate a server object
        httpd = HTTPServer (server_address, request_handler)
        print(time.asctime(), "Server Starting - %s:%s" % (self.host, self.port))

        try:
            # start serving pages
            httpd.serve_forever ()
        except KeyboardInterrupt:
            pass

        httpd.server_close()
        print(time.asctime(), "Server Stopped - %s:%s" % (self.host, self.port))