import unittest

from reportserver.server.PortsServiceHandler import PortsServiceHandler



class PortsServiceHandlerTest(unittest.TestCase):

    def testGetPort(self):
        portsServiceHandler = PortsServiceHandler()
        response = portsServiceHandler.getPortData(80)
        self.assertEqual(response, None)

