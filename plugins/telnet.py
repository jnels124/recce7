################################################################################
#                                                                              #
#                           GNU Public License v3.0                            #
#                                                                              #
################################################################################
#   HunnyPotRx is a honeypot designed to be a one click installable,           #
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

"""
"""

from plugins.base import BasePlugin
from socket import SocketIO


class TelnetPlugin(BasePlugin):
    def __init__(self, socket, config, framework):
        BasePlugin.__init__(self, socket, config, framework)
        self.input_type = ''
        self.user_input = ''
        self.io = SocketIO(self._skt, "rw")
        self._session = None

    def do_track(self):
        self.get_session()

        try:
            self.username()
            self.password()
            self.options()
            while self._skt and not self.kill_plugin:
                self.command()
        except OSError:
            self.kill_plugin = True
            self.io.close()
            return
        except AttributeError:
            self.kill_plugin = True
            self.io.close()
            return
        except UnicodeDecodeError:
            self.kill_plugin = True
            self.io.close()
            return

    def get_session(self):
        self._session = str(self.get_uuid4())

    def get_input(self):
        try:
            data = self.io.readline(1024).decode()
        except OSError:
            self.kill_plugin = True
            return

        data = data.strip('\r\n')
        data = data.strip('\n')
        return data

    def username(self):
        self.io.write(b'Username: ')

        self.input_type = 'username'
        self.user_input = self.get_input()
        self.do_save()

    def password(self):
        self.io.write(b'Password: ')

        self.input_type = 'password'
        self.user_input = self.get_input()
        self.do_save()

    def command(self):
        self.input_type = 'command'
        self.io.write(b'. ')

        self.user_input = self.get_input()
        arguments = self.user_input.split(' ', 1)

        if len(arguments) == 0:
            return

        self.user_input = arguments.pop(0)
        self.do_save()

        if hasattr(self, self.user_input):
            if hasattr(getattr(self,self.user_input),'is_command'):
                if len(arguments) == 0:
                    getattr(self,self.user_input)()
                else:
                    getattr(self,self.user_input)(arguments.pop(0))
            else:
                self.do_save()
                self.io.write(b'%unrecognized command - type options for a list\r\n')
        else:
            self.do_save()
            self.io.write(b'%unrecognized command - type options for a list\r\n')

    def set_command(function):
        function.is_command = True
        return function

    OPTIONS = ['options',
               'help',
               'echo',
               'quit']

    @set_command
    def options(self, arguments=None):
        self.io.write(b'\r\nWelcome, Please choose from the following options\r\n')
        for option in self.OPTIONS:
            option += '\t'
            self.io.write(option.encode())
        self.io.write(b'\r\n')

    @set_command
    def help(self, arguments=None):
        help_msg = b'echo:\t\tprompt to echo back typing\r\n' \
                   b'help:\t\tdetailed description of options\r\n' \
                   b'options:\tbasic list of options available to user\r\n' \
                   b'quit:\t\tclose telnet connection to server\r\n'
        self.io.write(help_msg)

    @set_command
    def echo(self, arguments=None):
        self.input_type = 'echo'
        if arguments:
            self.user_input = arguments
        else:
            self.io.write(b'Text? ')
            self.user_input = self.get_input()
        self.io.write(self.user_input.encode() + b'\r\n')
        self.do_save()

    @set_command
    def quit(self, arguments=None):
        self.io.write(b'\nGoodbye\n')
        self.io.close()
        self.kill_plugin = True