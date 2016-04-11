__author__ = 'Charlie Mitchell <belmontrevenge@gmail.com>'
'''
This class will handle any date/time requests from the webserver.
This includes calculating the date/time range for data to return,
as well as converting the string timestamp in the database.
'''

import datetime

from reportserver.manager.UnitOfMeasure import UnitOfMeasure


# Return the date for how far back to query DB.
# If not specified, defaults to 1 day.
def get_begin_date(unit="days", unit_size=1):
    unit = unit.lower()
    if unit == UnitOfMeasure.MINUTE.value:
        d = datetime.timedelta(minutes=unit_size)
    elif unit == UnitOfMeasure.HOUR.value:
        d = datetime.timedelta(hours=unit_size)
    elif unit == UnitOfMeasure.DAY.value:
        d = datetime.timedelta(days=unit_size)
    elif unit == UnitOfMeasure.WEEK.value:
        d = datetime.timedelta(weeks=unit_size)
    else:
        # If 'unit' not an accepted string, default to 1 day.
        d = datetime.timedelta(days=1)

    return calc_date(d)

def calc_date(delta):
    now = datetime.datetime.now()
    return (now - delta)

# Takes the datetime object and returns a string in ISO 8601 format.
def get_iso_format(begin_date):
    return begin_date.isoformat()