import queue

from common.globalconfig import GlobalConfig
from common.logger import Logger
from database import datavalidator

__author__ = 'Ben Phillips'

class DataQueue:
    def __init__(self):
        self.dataQueue = queue.Queue()
        self.dv = datavalidator.DataValidator()
        self.log = Logger().get('database.dataqueue.DataQueue')
    """we want to check the data here and fail early
        if the data is good then we want to put it in the data queue
        we will want another python script for the validations (datavalidator.py)
        we need to enforce type constraints because the database will not
        see datavalidator.py"""
    def insert_into_data_queue(self, value):
        if not self.dv.run_all_checks(value):
            self.log.error('--> Validation failed! Unable to add data '
                           'into data queue: ' +
                           str(value))
            return False
        try:
            self.dataQueue.put(value)
        except queue.Full as e:
            self.log.critical('Data queue is full!')
        finally:
            return True

    def get_next_item(self):
        item = self.dataQueue.get()
        self.dataQueue.task_done()
        return item

    def check_empty(self):
        result = self.dataQueue.empty()
        return result
