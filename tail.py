#!/usr/bin/env python

'''
Python-Tail - Unix tail follow implementation in Python. 
python-tail can be used to monitor changes to a file.
Example:
    import tail
    # Create a tail instance
    t = tail.Tail('file-to-be-followed')
    # Register a callback function to be called when a new line is found in the followed file. 
    # If no callback function is registerd, new lines would be printed to standard out.
    t.register_callback(callback_function)
    # Follow the file with 5 seconds as sleep time between iterations. 
    # If sleep time is not provided 1 second is used as the default time.
    t.follow(s=5) '''

# Author - Kasun Herath <kasunh01 at gmail.com>
# Source - https://github.com/kasun/python-tail

import log
import os
import sys
import time
from datetime import datetime

class Tail(object):
    ''' Represents a tail command. '''
    def __init__(self, tailed_file):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.
            
            Arguments:
                tailed_file - File to be followed. '''

        # self.check_file_validity(tailed_file)
        self.tailed_file = tailed_file
        self.callback = sys.stdout.write
        self.today = datetime.today()
        self.logger = log.get_logger()
        self.curr_position = 0

    def follow(self, s=1):
        ''' Do a tail follow. If a callback function is registered it is called with every new line. 
        Else printed to standard out.
    
        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1. '''

        # wailt until file is made by KFTP
        if not os.access(self.tailed_file, os.F_OK):
            time.sleep(600)
            return

        self.check_file_validity(self.tailed_file)
        while self.check_fin_condition():
            self.logger.debug("open")
            file_ = open(self.tailed_file, 'rt', encoding='cp949')
            file_.seek(self.curr_position)
            lines = file_.readlines()
            self.curr_position = file_.tell()
            self.logger.debug("close")
            file_.close()
            for line in lines:
                self.callback(line)
            time.sleep(s)

    def register_callback(self, func):
        ''' Overrides default callback function to provided function. '''
        self.callback = func

    def set_tailed_file(self, tf):
        self.logger.info("tail.py - set_tailed_file:" + tf)
        self.tailed_file = tf
    
    def set_today(self):
        self.today = datetime.today()

    def reset_curr_position(self):
        self.curr_position = 0

    def check_file_validity(self, file_):
        ''' Check whether the a given file exists, readable and is a file '''
        # if not os.access(file_, os.F_OK):
        #     raise TailError("File '%s' does not exist" % (file_))
        if not os.access(file_, os.R_OK):
            raise TailError("File '%s' not readable" % (file_))
        if os.path.isdir(file_):
            raise TailError("File '%s' is a directory" % (file_))
    
    def check_fin_condition(self):
        if self.today.day == datetime.today().day:
            return True
        return False

class TailError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message