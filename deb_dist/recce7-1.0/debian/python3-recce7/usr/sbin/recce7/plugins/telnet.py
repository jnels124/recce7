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


class TelnetPlugin(BasePlugin):
    def __init__(self, socket, config, framework):
        BasePlugin.__init__(self, socket, config, framework)
        self.input_type = None
        self.user_input = None
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
            return
        except AttributeError:
            self.kill_plugin = True
            return
        except UnicodeDecodeError:
            self.kill_plugin = True
            return

    def get_session(self):
        self._session = str(self.get_uuid4())

    def get_input(self):
        try:
            data = self._skt.recv(1024).decode()
        except OSError:
            self.kill_plugin = True
            return

        data = data.strip('\r\n')
        data = data.strip('\n')
        return data

    def username(self):
        self._skt.send(b'Username: ')

        self.input_type = 'username'
        self.user_input = self.get_input()
        self.do_save()

    def password(self):
        self._skt.send(b'Password: ')

        self.input_type = 'password'
        self.user_input = self.get_input()
        self.do_save()

    def command(self):
        self.input_type = 'command'
        self._skt.send(b'. ')

        self.user_input = self.get_input()
        self.do_save()
        arguments = self.user_input.split(' ', 1)

        if len(arguments) == 0:
            return

        try:
            getattr(self, arguments.pop(0))(arguments)
        except AttributeError:
            self._skt.send(b'%unrecognized command - type options for a list\r\n')

    OPTIONS = ['options',
               'help',
               'echo',
               'quit',]

    def options(self, arguments=None):
        self._skt.send(b'\r\nWelcome, Please choose from the following options\r\n')
        for option in self.OPTIONS:
            option += '\t'
            self._skt.sendall(option.encode())
        self._skt.send(b'\r\n')

    def help(self, arguments=None):
        help_msg = b'echo:\t\tprompt to echo back typing\r\n' \
                   b'help:\t\tdetailed description of options\r\n' \
                   b'options:\tbasic list of options available to user\r\n' \
                   b'quit:\t\tclose telnet connection to server\r\n'
        self._skt.send(help_msg)

    def echo(self, arguments=None):
        if len(arguments) > 0:
            for i in arguments:
                self._skt.send(i.encode())
        else:
            self._skt.send(b'Text? ')
            self.input_type = 'echo'
            self.user_input = self.get_input()
            self._skt.send(self.user_input.encode())
            self.do_save()
        self._skt.send(b'\r\n')

    def quit(self, arguments=None):
        self._skt.send(b'\nGoodbye\n')
        self.kill_plugin = True