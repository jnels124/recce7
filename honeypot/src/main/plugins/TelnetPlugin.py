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
import uuid

# import telnetsrv
# from telnetsrv.threaded import TelnetHandler, command
from plugins.BasePlugin import BasePlugin
import datetime


class TelnetPlugin(BasePlugin):
    def __init__(self, socket, framework):
        print('Spawned TelnetPlugin!')
        self.frmwk = framework
        BasePlugin.__init__(self, socket, framework)

    # @command('echo')
    # def command_echo(self, params):
    #     '''<text to echo>
    #     Echo text back to the console.
    #     This command simply echos the provided text
    #     back to the console.
    #     '''
    #     pass
    #
    # @command('info')
    # def command_info(self, params):
    #     '''
    #     Provides some information about the current terminal.
    #     '''
    #     self.writeresponse( "Username: %s, terminal type: %s" % (self.username, self.TERM) )
    #     self.writeresponse( "Command history:" )
    #     for c in self.history:
    #         self.writeresponse("  %r" % c)



    def do_track(self):
        welcome = 'Welcome to %s\n' % self._localAddress
        self._skt.send(welcome.encode())
        escape = b'\x1e'
        data = ''
        self.user_input = 'BEGIN USER DATA ::'
        # b'' is what I am getting back when the user calls close from the local telnet prompt, may want to look at
        # reading FIN signals from socket somehow, but this works for now
        while data != escape and data != b'':
            data = self._skt.recv(1024)
            self.user_input += '\n%s' % data
            self._skt.sendall(data)

        self._skt.send(b'\nGoodbye.\n')
        self.form_data_for_insert(self.user_input)

    def form_data_for_insert(self, raw_data):
        # Would like to be able to read config data from either base or framework if possible, would also like table
        # name derived from elsewhere
        event_time = datetime.datetime.now().isoformat()
        data = {'test_telnet': {'User_Data': raw_data, 'Test_col': 'This is a test', 'eventdatetime': event_time}}
        self.do_save(data)