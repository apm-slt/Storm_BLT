#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : ddrshmoo_testcase.py
Description:
'''

import os
import sys
import re
import time
import pexpect
from bench_info import *
from pwrctl_OFF import *
from pwrctl_ON import *
from global_define import *
from totaltime import totaltime_taken
from test_summary import *


def pcie_calib_testcase(FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   pcie_calib_slimpro_cmd = 'sudo minicom -D ' + uart_port_ttyS3 + ' -C ' + minicom_cap_slimpro
   pcie_calib_dut_cmd = 'sudo minicom -D ' + uart_port_ttyS2 + ' -C ' + logfile
   os.environ['TERM'] = 'vt100'
   try:
      pcie_calib_dut_process = pexpect.spawn(pcie_calib_dut_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START DUT PROCESS"
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()
   try:
      pcie_calib_slimpro_process = pexpect.spawn(pcie_calib_slimpro_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START SLIMPRO PROCESS"
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()
   pcie_calib_slimpro_process.delaybeforesend=1
   pcie_calib_dut_process.delaybeforesend=1
   power_cycle=int(ddr_power_cycle_count) 
   print "\n"
   print "="*60
   print "      PCIE CALIB Test with Power Recycling    "
   print "                                             "
   print "--> No. of power recycles    : ",power_cycle
   print "="*60
   m=0
   while m<power_cycle:
      print bcolors.OKBLUE +"\n== POWER CYCLE:",int(m+1)," ==" + bcolors.ENDC
      power_OFF(cfgfile)
      time.sleep(5)
      power_ON(cfgfile)

      index = 100
      index=pcie_calib_slimpro_process.expect([pexpect.TIMEOUT, 'Boot.*from.*SPI-NOR'], timeout=60)
      if index == 0:
         print "INFO: Slimpro doesn't boot"
         power_OFF(cfgfile)
         test_summary(logfile, ip_list, test_result_map, FA_comments)
         totaltime_taken(logfile)
         sys.exit()
      time.sleep(5)
      pcie_calib_slimpro_process.sendline('y\r')
      time.sleep(1)
      print "INFO: SLIMPRO PROCESS IS DONE!"

      index=100
      index=pcie_calib_dut_process.expect([pexpect.TIMEOUT, 'cold reset', 'FAILED','Mustang#'], timeout=200)
      if index == 0:
         print "INFO: U-boot doesn't boot.  Timeout"
         test_result_map['pcie_calib']= 'FAIL'
         test_summary_map['pcie_calib']= 'FAIL'
      elif index == 1:
         print "INFO: U-boot cold reset."
         test_result_map['pcie_calib']= 'FAIL'
         test_summary_map['pcie_calib']= 'FAIL'
      elif index == 2:
         test_result_map['pcie_calib']= 'FAIL'
         test_summary_map['pcie_calib']= 'FAIL'
         print bcolors.FAIL + "INFO: PCIE CALIB IN U-BOOT:",test_result_map['pcie_calib'] + bcolors.ENDC
         index = 100
         index=pcie_calib_dut_process.expect([pexpect.TIMEOUT, 'Mustang#'],timeout=120)
         if index == 1:
            print "INFO: >>> U-BOOT BOOTED UP SUCCESSFULLY! <<<"   
      elif index == 3:
         print "INFO: >>> U-BOOT BOOTED UP SUCCESSFULLY! <<<"
         if test_result_map['pcie_calib'] != 'FAIL':
            test_result_map['pcie_calib'] = 'PASS'
            if test_summary_map['pcie_calib']== 'FAIL':
               test_summary_map['pcie_calib'] = 'FAIL'
            else:
               test_summary_map['pcie_calib'] = 'PASS'
            print bcolors.OKGREEN + "INFO: PCIE CALIB IN U-BOOT:",test_result_map['pcie_calib'] + bcolors.ENDC
      time.sleep(1)
      m+=1
   pcie_calib_dut_process.close()
   pcie_calib_slimpro_process.close()
   power_OFF(cfgfile)
   if (test_type == "Screen" and test_result_map['pcie_calib'] != 'FAIL'):
      print "Test exiting..."
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()
