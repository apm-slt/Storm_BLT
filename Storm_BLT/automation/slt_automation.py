#! /usr/bin/env python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : slt_automation.py
Description:
'''

import os
import sys
import re
import time
import pexpect
from vbios_testcase import *
from ddrshmoo_testcase import *
from memtester_testcase import *
from pmd_testcase import *
from bench_info import *
from global_define import *
from test_summary import *
from totaltime import totaltime_taken
from pcie_calib_testcase import *

def main():
   '''
   This automation framework includes the screen tests in vbios, ubsa, and linux environment.  All of the IP tests are in vbios environment.  DDR
   shmoo test is in ubsa and linux memtest is in linux environment. It is good to stress or screen the parts in different environents to give more   environment coverage.  
   user: the operator name
   ip  : the blt/slt bench IP address
   nps : remote power switch IP address
   vbios_prompt:  vbios prompt signature
   p_port: nps power port id
   DPC: DIMM per Channel configuration on blt/slt bench
   lot_no: the lot number of the screened parts
   build_id: control vbios build revision
   test_type: either "ES" mode or "production" mode.  "ES" mode is engineer sample FA mode which will not stop on fail.  "production" mode is 
   stop on fail.
   screen_option: either "ddr_only" or "full_screen" or "vbios_only".  "ddr_only" mode tests ddr margin shmoo test and linux memtester, they 
   will not include the vbios tests. "full_screen" mode tests both vbios tests and ddr shmoo as well as linux memtester - They are the default
   option to give full test coverages.  "vbios_only" mode tests only SOC IPs - they do not test ddr memory.
   FA: the failure analysis mode prompt users to enter any useful information about the parts which users will perform.
   uart_port_ttyS2: dut access uart
   uart_port_ttyS3: slimpro access uart
   minicom_cap_slimpro: capture file which use in slimpro during spawn process
   vbios_power_cycle_count: vbios tests power cycles which allow users to specify how many power cycles.  Useful mode in regression
   ddr_power_cycle_count: ddr tests power cycles which allow users to specify how many power cycles.  Useful mode in regression
   linux_power_cycle_count: linux ddr memtester test allow users to specify how many power cycles.  Useful mode in regression    
   '''
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   
   '''
   if test_type is production, this is will be testing one test case at a time 
      and will be stop on fail
   '''
   if FA == 'YES':
      print "-"*99
      FA_comments = raw_input("If this is the Failure Analysis, Please enter some comments.  Hit Enter when done....  \n")
      print "-"*99
      print "\n"
   else:
      FA_comments = 'No Label'

   clearfile=open(minicom_cap_slimpro, 'r+')
   clearfile.truncate()
   clearfile.close()
   if (screen_option == "vbios_only"):
      vbios_testcase(bench_map, FA_comments)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
   elif (screen_option == "ddr_only") :
      ddrshmoo_testcase(FA_comments)
      time.sleep(20)
      memtester_testcase(FA_comments)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
   else:
      vbios_testcase(bench_map, FA_comments)
      time.sleep(20)
      ddrshmoo_testcase(FA_comments)
      time.sleep(20)
      memtester_testcase(FA_comments)
      time.sleep(20)
      pmd_testcase(FA_comments)
      time.sleep(20)
      if DPC == 1:
         pcie_calib_testcase(FA_comments)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
if __name__=='__main__':
   main()

