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
from common.GlobalConfig import Configuration
from reportserver.dao import DatabaseHandler


class PortManager:

    # Port Manager: calls necessary managers and utilities to generate parameters for sql.
    # List of valid ports it can receive is taken from the Configuration setup.
    #
    #
    validPortNumbers = ()

    def __init__(self):
        self.g_config = Configuration().getInstance()
        self.validPortNumbers = self.g_config.get_ports()


    def isPortValid(self, port_number):
        if (port_number in self.validPortNumbers):
            return True
        else:
            return False

    def getPort(self, port_number, uom, unit):
        print("Retrieving port:" + str(port_number) + "uom:" + uom + " size: " + str(unit))

        if self.isPortValid(port_number):
            return DatabaseHandler.get_json_by_time(port_number, uom, unit)
        else:
            return None


