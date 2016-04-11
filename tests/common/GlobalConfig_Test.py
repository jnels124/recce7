from common.GlobalConfig import Configuration
import unittest;

test_cfg_path = 'tests/common/test.cfg'


class GlobalConfig_Test(unittest.TestCase):
    def setUp(self):
        self.gconfig = Configuration(test_cfg_path).getInstance()

    def test_getInstance(self):

        gconfig2 = Configuration().getInstance()

        self.assertEqual(str(self.gconfig),str(gconfig2),"these 2 objects should equal")

        gconfig3 = Configuration().getInstance()

        self.assertEqual(str(self.gconfig), str(gconfig3), "these 2 objects should equal")
        self.assertEqual(str(gconfig2), str(gconfig3), "these 2 objects should equal")


    def test_getPorts(self):

        ports = self.gconfig.get_ports()

        self.assertEqual(len(ports), 2, "expected 2 ports in test.cfg found: " + str(len(ports)))

        for port in ports:
            print("found: " + str(port))


    def test_getReportServerConfig(self):
        host = self.gconfig.get_report_server_host()
        port = self.gconfig.get_report_server_port()
        self.assertEqual(host, "", "expected host to be ''")
        self.assertEqual(port, 8080, "expected port to be '8080' ")

    def test_getReportServerHost(self):
        self.assertEqual("", self.gconfig.get_report_server_host())

    def test_getReportServerPort(self):
        self.assertEqual(8080, self.gconfig.get_report_server_port())

    def test_refresh_instance(self):

        gconfig2 = Configuration(test_cfg_path, True).getInstance()
        self.assertNotEqual(str(self.gconfig), str(gconfig2), "these 2 objects should NOT equal when refresh set to True")

    def test_refresh_instance_same(self):
        gconfig2 = Configuration(test_cfg_path, False).getInstance()
        self.assertEqual(str(self.gconfig), str(gconfig2), "these 2 objects should equal when False is set for Refresh")

        gconfig2 = Configuration(test_cfg_path).getInstance()
        self.assertEqual(str(self.gconfig), str(gconfig2), "these 2 objects should equal with default of False")

    def test_get_date_time_name(self):
        self.assertEqual("eventDateTime", self.gconfig.get_db_datetime_name())

    def test_get_db_peerAddress_nameself(self):
        self.assertEqual("peerAddress", self.gconfig.get_db_peerAddress_name())

    def test_get_db_localAddress_name(self):
        self.assertEqual("localAddress", self.gconfig.get_db_localAddress_name())


if __name__ == "__main__":
    unittest.main()
