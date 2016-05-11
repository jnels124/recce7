################################################################################
#                                                                              #
#                           GNU Public License v3.0                            #
#                                                                              #
################################################################################
#   HunnyPotR is a honeypot designed to be a one click installable,            #
#   open source honey-pot that any developer or administrator would be able    #
#   to write custom plugins for based on specific needs.                       #
#   Copyright (C) 2016 RECCE7                                                  #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See their            #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public licenses         #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
################################################################################
from common.logger import Logger
from common.globalconfig import GlobalConfig
from reportserver.dao.DatabaseHandler import DatabaseHandler
from reportserver.manager import dateTimeUtility
from reportserver.manager import utilities

import dateutil.parser


class PortManager:

    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    # List of valid ports it can receive is taken from the Configuration setup.
    #
    validPortNumbers = ()

    def __init__(self):
        self.g_config = GlobalConfig()
        self.validPortNumbers = self.g_config.get_ports()
        self.date_time_field = self.g_config.get_db_datetime_name()
        self.log = Logger().get('reportserver.manager.PortManager.PortManager')


    def isPortValid(self, port_number):
        if (port_number in self.validPortNumbers):
            return True
        else:
            return False

    def getPort(self, port_number, uom, unit):
        self.log.info("Retrieving port:" + str(port_number) + "uom:" + uom + " size: " + str(unit))

        items = []

        if self.isPortValid(port_number):
            results = DatabaseHandler().get_json_by_time(port_number, uom, unit)
            items = utilities.process_data(results)

        port_json = {
            'port': str(port_number),
            'timespan': uom + "=" + str(unit),
            'items':items
        }

        return port_json


    def get_port_attack_count(self, tablename, unit, uom):
        fromDate = dateTimeUtility.get_begin_date_iso(unit, uom)

        sql = "select count(distinct session) as total_attacks from %s where %s >= '%s' " %(tablename, self.date_time_field, fromDate)
        self.log.debug("sql is:" + sql)
        result = DatabaseHandler().query_db(sql)[0]
        return int(result['total_attacks'])

    def get_unique_ips(self, tablename, unit, uom):
        fromDate = dateTimeUtility.get_begin_date_iso(unit, uom)
        sql = "select count(distinct peerAddress) as unique_ips from %s where %s >= '%s' " % (tablename, self.date_time_field, fromDate)
        self.log.debug("sql is:" + sql)
        result = DatabaseHandler().query_db(sql)[0]
        return int(result['unique_ips'])


