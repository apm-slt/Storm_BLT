#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : ddrshmoo_no_test_pass_fail.py
Description:
'''

import os
from bench_info import *
from global_define import *

def ddrshmoo_no_test_pass_fail(filename):
   fd=open(filename, 'a')
   print >> fd, "\n"
   print >> fd, "-"*60
   print >> fd, "Total No. of DDR SHMOO Pass Test: %s"%ddrshmoo_no_test_pass_fail_map['PASS']
   print >> fd, "Total No. of DDR SHMOO Fail Test: %s"%ddrshmoo_no_test_pass_fail_map['FAIL']
   print >> fd, "\n"
   fd.close()

