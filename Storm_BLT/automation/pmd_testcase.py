#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : pmd_testcase.py
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
from cmd_images import *
from global_define import *
from pmd_no_test_pass_fail import *
from totaltime import totaltime_taken
from pmd_system_exit import pmd_system_exit

def pmd_testcase(FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   cmd_images_dict, cmd_images_list=cmd_images(cmd_images_file)
   pmd_slimpro_cmd = 'sudo minicom -D ' + uart_port_ttyS3 + ' -C ' + minicom_cap_slimpro
   pmd_dut_cmd = 'sudo minicom -D ' + uart_port_ttyS2 + ' -C ' + logfile
   os.environ['TERM'] = 'vt100'
   try:
      pmd_dut_process = pexpect.spawn(pmd_dut_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START DUT PROCESS"
      pmd_system_exit(FA_comments)
   try:
      pmd_slimpro_process = pexpect.spawn(pmd_slimpro_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START SLIMPRO PROCESS"
      pmd_system_exit(FA_comments)
   pmd_slimpro_process.delaybeforesend=1
   pmd_dut_process.delaybeforesend=1

   power_cycle=int(linux_power_cycle_count)
   print "\n"
   print "="*60
   print "      PMD Test with Power Recycling    "
   print "                                             "
   print "--> No. of power recycles    : ",power_cycle
   print "="*60
   t=0
   while t<power_cycle:
      print bcolors.OKBLUE +"\n== POWER CYCLE:",int(t+1)," ==" + bcolors.ENDC
      power_OFF(cfgfile)
      time.sleep(5)
      power_ON(cfgfile)

      index = 100
      index=pmd_slimpro_process.expect([pexpect.TIMEOUT, 'Boot.*from.*SPI-NOR'], timeout=60)
      if index == 0:
         print "INFO: Slimpro doesn't boot"
         pmd_system_exit(FA_comments)
      time.sleep(5)
      pmd_slimpro_process.sendline('y\r')
      time.sleep(1)
      print "INFO: SLIMPRO PROCESS IS DONE!"

      index=100
      index=pmd_dut_process.expect([pexpect.TIMEOUT, 'cold reset', 'Mustang#'], timeout=120)
      if index == 0:
         print "INFO: U-boot doesn't boot"
         pmd_boot_fail = int(1)
         pmd_system_exit(FA_comments)
      elif index == 1:
         print "INFO: U-boot cold reset"
         pmd_boot_fail = int(1)
         pmd_system_exit(FA_comments)
      print "INFO: >>> U-BOOT BOOTED UP SUCCESSFULLY! <<<"
      time.sleep(1)
      print "INFO: PMD Testing..."
      pmd_dut_process.sendline('tftp 0x001d000000 ' + cmd_images_dict['pmd_test_binary'] +'\r')
      pmd_dut_process.expect('Mustang#')
      time.sleep(1)
      pmd_dut_process.sendline('go 0x1d000000\r')
      pmd_dut_process.expect('ubsa #')
      time.sleep(1)
      pmd_dut_process.sendline(cmd_images_dict['pmd_cmd'] + ' ' + cmd_images_dict['no_thread']  + '\r')
      index=100
      index=pmd_dut_process.expect([pexpect.TIMEOUT, 'pmd_test: passed: error_status=0', 'pmd_test: failed', 'Exception'], timeout=120)
      if index == 0:
         print "INFO: PMD Test timeout"
         test_result_map['pmd'] = 'FAIL'
         test_summary_map['pmd'] = 'FAIL'
         print bcolors.FAIL + "INFO: PMD TEST:",test_result_map['pmd'] + bcolors.ENDC
         pmd_no_test_pass_fail_map['FAIL']+=1
         pmd_system_exit(FA_comments)
      elif index == 1:
         test_result_map['pmd'] = 'PASS'
         if test_summary_map['pmd'] == 'FAIL':
            test_summary_map['pmd'] = 'FAIL'
         else:
            test_summary_map['pmd'] = 'PASS'
         print bcolors.OKGREEN + "INFO: PMD TEST:",test_result_map['pmd'] + bcolors.ENDC
         pmd_no_test_pass_fail_map['PASS']+=1
      else:
         print "INFO: PMD TEST FAIL"
         test_result_map['pmd'] = 'FAIL'
         test_summary_map['pmd'] = 'FAIL'
         print bcolors.FAIL + "INFO: PMD TEST:",test_result_map['pmd'] + bcolors.ENDC
         pmd_no_test_pass_fail_map['FAIL']+=1
         pmd_system_exit(FA_comments)
      t+=1
   pmd_no_test_pass_fail(logfile)
   print "-"*60
   print "Total No. of PMD Test Pass Test: %s"%pmd_no_test_pass_fail_map['PASS']
   print "Total No. of PMD Test Fail Test: %s"%pmd_no_test_pass_fail_map['FAIL']
   print "\n"   
   power_OFF(cfgfile)
   if (test_type == "Screen" and pmd_no_test_pass_fail_map['FAIL'] == int(1)):
      print "Test exiting..."
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()


