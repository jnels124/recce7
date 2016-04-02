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
from plugins.base import BasePlugin


class TelnetPlugin(BasePlugin):
    def __init__(self, socket, framework):
        super().__init__(socket, framework)
        self._framework = framework
        self.username = "NULL"
        self.password = "NULL"

    def login(self):
        user_prompt = "Username: "
        pw_prompt = "Password: "

        for prompt in [user_prompt, pw_prompt]:
            try:
                self._skt.send(prompt.encode())
                if prompt == pw_prompt:
                    self.password = self._skt.recv(1024).decode().replace('\r\n', '')
                else:
                    self.username = self._skt.recv(1024).decode().replace('\r\n', '')
            except OSError as e:
                if not self._skt:
                    # TODO log that the socket was closed
                    pass
                raise e
            except AttributeError as ae:
                # TODO log was not able to capture the either the username or password properly so decode fails
                raise ae

    def do_track(self):

        # user options
        opt = 'options'
        hlp = 'help'
        ech = 'echo'
        qt = 'quit'
        options_list = [opt, hlp, ech, qt]
        uo = useroptions(self._skt)

        self.login()
        uo.options(options_list, True)

        user_input = ''
        while not self.kill_plugin:
            try:
                self._skt.send(b'.')
                data = self._skt.recv(1024).decode()
                d = data.replace('\r\n', '')

                if d in options_list:
                    if d == opt:
                        uo.options(options_list, False)
                    elif d == hlp:
                        uo.help()
                    elif d == ech:
                        data = uo.echo()
                    elif d == qt:
                        self.kill_plugin = uo.quit()

            except OSError as e:
                if not self._skt:
                    break
                raise e

            user_input += '%s' % data

        if self._skt:
            self._skt.send(b'\nGoodbye.\n')
        self._skt = None
        self.form_data_for_insert(user_input)

    def form_data_for_insert(self, raw_data):
        data = {'test_telnet': {'User_Data': raw_data, 'User_Name': self.username, 'Password': self.password}}
        self.do_save(data)


class useroptions(TelnetPlugin):
    def __init__(self, socket):
        self._skt = socket

    def options(self, options_list, is_login):
        if is_login:
            self._skt.send(b'\r\nWelcome, Please choose from the following options\r\n')
        for opt in options_list:
            opt += '\t'
            self._skt.sendall(opt.encode())
        self._skt.send('\n'.encode())

    def help(self):
        help_msg = b'Command echo:\t\tprompt to echo back typing\r\nCommand help:\t\tdetailed description of ' \
                   b'options\r\nCommand options:\tbasic list of options available to user\r\nCommand quit:\t\t' \
                   b'close telnet connection to server\r\n'
        self._skt.send(help_msg)

    def echo(self):
        self._skt.sendall('text? '.encode())
        try:
            data = self._skt.recv(1024).decode()
        except OSError as e:
            # TODO log error here
            raise e
        self._skt.sendall(data.encode())
        return data

    def quit(self):
        return True