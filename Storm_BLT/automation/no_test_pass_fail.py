#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : no_test_pass_fail.py
Description:
'''

import os
from bench_info import *
from global_define import *

def no_test_pass_fail(filename):
   fd=open(filename, 'a')
   print >> fd, "\n"
   print >> fd, "-"*60
   print >> fd, "Total No. of VBIOS Pass Test: %s"%no_test_pass_fail_map['PASS']
   print >> fd, "Total No. of VBIOS Fail Test: %s"%no_test_pass_fail_map['FAIL']
   print >> fd, "\n"
   fd.close()

