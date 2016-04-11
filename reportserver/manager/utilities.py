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


#Given a string, try to convert it to an int.
def validatePortNumber(givenStr):
    print("given str is: " + givenStr)
    try:
        return int(givenStr)
    except Exception as e:
        print("Received invalid string to convert to int: " + givenStr)
        print (str(e))
        return None


#Given a token
def validateTimePeriod(tokens):
    #TODO:  validate the tokens given.
    if len(tokens) != 7:
        raise ValueError("token length expected is 7")

    uom = None
    units = None

    uom = str(tokens[5])
    units = int(tokens[6])

    print(uom + ": " + str(units))
    return (uom, units)
