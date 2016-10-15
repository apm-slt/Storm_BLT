#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : totaltime.py
Description:
'''

import os
import sys
import re
import time
from datetime import timedelta
import pexpect
from global_define import *

def totaltime_taken(filename):
   fd=open(filename, 'a')
   totaltime_taken = str(timedelta(seconds=(time.time()-start)))
   print "\nTOTAL TIME TAKEN: {}\n".format(totaltime_taken)
   print >>fd, "\nTOTAL TIME TAKEN: {}\n".format(totaltime_taken)
   fd.close()
   
      
