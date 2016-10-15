#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : vbios_testcase.py
Description:
'''

import os
import sys
import re
import time
import pexpect
from headerfile import *
from pwrctl_OFF import *
from pwrctl_ON import *
from bench_info import *
from global_define import *
from test_L1 import *
from test_L import *
from cmd_selected import *
from no_test_pass_fail import *
from vbios_system_exit import vbios_system_exit

def vbios_testcase(bench_map, FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   if bench_map[b_num] == 'test_L1':
      test_list=test_L1(test_L1_file)
   else:
      test_list=test_L(test_L_file)
   '''
   if FA == 'YES':
      print "-"*99
      FA_comments = raw_input("If this is the Failure Analysis, Please enter some comments.  Hit Enter when done....  \n")
      print "-"*99
      print "\n"
   '''
   slimpro_cmd = 'sudo minicom -D ' + uart_port_ttyS3 + ' -C ' + minicom_cap_slimpro
   dut_cmd = 'sudo minicom -D ' + uart_port_ttyS2 + ' -C ' + logfile 
   os.environ['TERM'] = 'vt100'
   try:
      dut_process = pexpect.spawn(dut_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START DUT PROCESS"
      vbios_system_exit(FA_comments)
   try:
      slimpro_process = pexpect.spawn(slimpro_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START SLIMPRO PROCESS"
      vbios_system_exit(FA_comments)
   slimpro_process.delaybeforesend=1
   #slimpro_process.logfile=sys.stdout
   dut_process.delaybeforesend=1
   #dut_process.logfile=sys.stdout
   index = 100
   slimpro_process.expect(':', timeout=60)
   slimpro_process.sendline('amcc1234\r')
   dut_process.expect(':', timeout=60)
   dut_process.sendline('amcc1234\r')
   headerfile(logfile, FA_comments)

   power_cycle_count=int(vbios_power_cycle_count) 
   print "\n"
   print "="*60
   print "      VBIOS Test with Power Recycling                          "
   print "                                                               "
   print "--> No. of power recycles    : ",power_cycle_count
   print "="*60
   n=0
   while n<power_cycle_count:
      print "Test List =%s"%test_list
      print bcolors.OKBLUE + "\n== POWER CYCLE:",int(n+1)," ==" + bcolors.ENDC
      power_OFF(cfgfile)
      time.sleep(5)
      power_ON(cfgfile)
      
      index = 100
      #index=slimpro_process.expect([pexpect.TIMEOUT, ':'], timeout=60)
      index=slimpro_process.expect([pexpect.TIMEOUT, 'Boot.*from.*SPI-NOR'], timeout=60)
      if index == 0:
         print "INFO: Slimpro doesn't boot"
         vbios_boot_fail = int(1)
         vbios_system_exit(FA_comments)
      time.sleep(5)
      slimpro_process.sendline('n\r')
      time.sleep(1)
      print "INFO: SLIMPRO PROCESS IS DONE!"

      index=100
      index=dut_process.expect([pexpect.TIMEOUT,'MCU UNCORRECTABLE ERR',vbios_prompt], timeout=60)
      if index == 0:
         print "INFO: Vbios doesn't boot"
         vbios_boot_fail = int(1)
         vbios_system_exit(FA_comments)
      elif index == 1:
         print "INFO: Vbios doesn't boot"
         vbios_boot_fail = int(1)
         vbios_system_exit(FA_comments)
      print "INFO: >>> VBIOS BOOTED UP SUCCESSFULLY! <<<"
      time.sleep(2)
      cmd_selected(test_list, dut_process, FA_comments)
      no_test_pass_fail(logfile)
      print "-"*60
      print "Total No. of VBIOS Pass Test: %s"%no_test_pass_fail_map['PASS']
      print "Total No. of VBIOS Fail Test: %s"%no_test_pass_fail_map['FAIL']
      print "\n"
      n+=1
   #power_OFF(cfgfile)  #FIX ME, remove if include ddr shmoo test
   dut_process.close()
   slimpro_process.close()

