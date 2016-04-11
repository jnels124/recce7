import unittest
import sys
from reportserver.manager import utilities

# Unit tests for utililties.py

class Utilities_Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_validate_port_number(self):
        result = utilities.validatePortNumber("200")
        self.assertEqual(200,result,"expected an integer of 200")

        result = utilities.validatePortNumber("abc")
        self.assertEqual(None, result, "expected None")

        result = utilities.validatePortNumber(str(sys.maxsize + 100) )
        self.assertEqual(sys.maxsize + 100, result, "expected system maxsize + 100")

if __name__ == "__main__":
    unittest.main()