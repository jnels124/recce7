import unittest
import datetime
from reportserver.manager import dateTimeUtility

# Unit tests for DateTimeUtility

class DateTimeTest(unittest.TestCase):

    #The date checks ignore milliseconds, since we are just trying to get the correct date.

    def test_get_begin_date(self):

        # Test with weeks
        d = datetime.timedelta(weeks=3)
        calculated_date = dateTimeUtility.get_begin_date("weeks", 3)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(weeks=7)
        calculated_date = dateTimeUtility.get_begin_date("weeks", 7)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(weeks=0)
        calculated_date = dateTimeUtility.get_begin_date("weeks", 0)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        # Test with days
        d = datetime.timedelta(days=5)
        calculated_date = dateTimeUtility.get_begin_date("days", 5)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(days=20)
        calculated_date = dateTimeUtility.get_begin_date("days", 20)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        calculated_date = dateTimeUtility.get_begin_date("days", 0)
        d = datetime.timedelta(days=0)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(days=1)
        calculated_date = dateTimeUtility.get_begin_date(unit="days")
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        calculated_date = dateTimeUtility.get_begin_date()
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        # Test with hours
        d = datetime.timedelta(hours=2)
        calculated_date = dateTimeUtility.get_begin_date("hours", 2)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))


        d = datetime.timedelta(hours=23)
        calculated_date = dateTimeUtility.get_begin_date("hours", 23)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(hours=0)
        calculated_date = dateTimeUtility.get_begin_date("hours", 0)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        # Test with minutes
        d = datetime.timedelta(minutes=45)
        calculated_date = dateTimeUtility.get_begin_date("minutes", 45)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        d = datetime.timedelta(minutes=88)
        calculated_date = dateTimeUtility.get_begin_date("minutes", 88)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))


        d = datetime.timedelta(minutes=0)
        calculated_date = dateTimeUtility.get_begin_date("minutes", 0)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        # Test default (1 day)
        d = datetime.timedelta(days=1)
        calculated_date = dateTimeUtility.get_begin_date("decades", 45)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        calculated_date = dateTimeUtility.get_begin_date("iemclaiejfkd djeaa", 2)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        calculated_date = dateTimeUtility.get_begin_date("", 30)
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

        calculated_date = dateTimeUtility.get_begin_date()
        self.assertEqual((self.format_date(calculated_date)), self.getDeltaOfDateNow(d))

    def getDeltaOfDateNow(self, delta):

        return self.format_date(datetime.datetime.now() - delta)


    def format_date(self,date_given):
        return date_given.strftime("%Y-%m-%d_%H:%M:%S")


    def test_get_iso_format(self):

        test_date = datetime.datetime(1999, month=12, day=31, hour=23, minute=59, second=59)
        test_iso = "1999-12-31T23:59:59"
        self.assertEqual(dateTimeUtility.get_iso_format(test_date), test_iso)

if __name__ == "__main__":
    unittest.main()