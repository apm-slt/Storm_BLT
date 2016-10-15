#!/usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : test_summary.py
Description:
'''

import os
import sys
import re
import time
import pexpect
from global_define import *
from get_bin2 import *
import generate_csv

def test_summary(filename, ip_list, test_result_map, FA_comments):
   os.chmod(filename, 777)
   fd=open(filename, 'a')
 
   print "============ Bench-%s: TEST SUMMARY =============="%b_num
   print >> fd ,"============ Bench-%s: TEST SUMMARY =============="%b_num
   print bcolors.UNDERLINE + "2DPC BENCH" + bcolors.ENDC
   print >> fd, "2DPC BENCH" 

   for x in ip_list:
      y=ip_map[x]
      if y == "PCIE EXTERNAL LOOPBACK GEN3":
         print bcolors.UNDERLINE + "1DPC BENCH" + bcolors.ENDC
         print >> fd, "1DPC BENCH"
      elif y== "DDR SHMOO TEST":
         print bcolors.UNDERLINE + "PMD and DDR" + bcolors.ENDC
         print >> fd, "PMD and DDR"
      if test_summary_map[x] == "PASS":
         print "{0:30} {1:2}".format(y,":") + bcolors.OKGREEN + test_summary_map[x] + bcolors.ENDC
         print >> fd, "{0:30} {1:2}".format(y,":")+test_summary_map[x]
      elif test_summary_map[x] == "FAIL":
         print "{0:30} {1:2}".format(y,":") + bcolors.FAIL + test_summary_map[x] + bcolors.ENDC
         print >> fd, "{0:30} {1:2}".format(y,":") + test_summary_map[x] 
      else:
         print "{0:30} {1:2}".format(y,":") + test_summary_map[x]
         print >> fd, "{0:30} {1:2}".format(y,":") + test_summary_map[x]
   print "="*40
   print >> fd, "="*40
   fd.close()
   if vbios_boot_fail == int(0) and ddrshmoo_boot_fail == int(0) and memtester_boot_fail == int(0) and pmd_boot_fail == int(0):
      get_bin2(filename)
   '''update csv file '''
   generate_csv.generate_csv(filename,"Bench-%s"%b_num, FA_comments)


