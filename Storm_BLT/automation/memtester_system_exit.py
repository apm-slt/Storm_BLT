#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : memtester_system_exit.py
Description:
'''

from pwrctl_OFF import *
from global_define import *
from totaltime import totaltime_taken
from memtester_no_test_pass_fail import *
from test_summary import *


def memtester_system_exit(FA_comments):
   print "exiting..."
   power_OFF(cfgfile)
   memtester_no_test_pass_fail(logfile)
   print "-"*60
   print "Total No. of DDR MEMTESTER Pass Test: %s"%memtester_no_test_pass_fail_map['PASS']
   print "Total No. of DDR MEMTESTER Fail Test: %s"%memtester_no_test_pass_fail_map['FAIL']
   print "\n"
   test_summary(logfile, ip_list, test_result_map, FA_comments)
   totaltime_taken(logfile)
   sys.exit()
   
