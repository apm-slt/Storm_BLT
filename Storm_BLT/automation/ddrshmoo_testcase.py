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
from cmd_images import *
from global_define import *
from ddrshmoo_no_test_pass_fail import *
from ddrshmoo_system_exit import ddrshmoo_system_exit

def ddrshmoo_testcase(FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   cmd_images_dict, cmd_images_list=cmd_images(cmd_images_file)
   '''
   if (screen_option == "ddr_only"):
      if FA == 'YES':
          print "-"*99
          FA_comments = raw_input("If this is the Failure Analysis, Please enter some comments.  Hit Enter when done....  \n")
          print "-"*99
          print "\n"
   '''
   ddr_slimpro_cmd = 'sudo minicom -D ' + uart_port_ttyS3 + ' -C ' + minicom_cap_slimpro
   ddr_dut_cmd = 'sudo minicom -D ' + uart_port_ttyS2 + ' -C ' + logfile
   os.environ['TERM'] = 'vt100'
   try:
      ddr_dut_process = pexpect.spawn(ddr_dut_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START DUT PROCESS"
      ddrshmoo_system_exit(FA_comments)
   try:
      ddr_slimpro_process = pexpect.spawn(ddr_slimpro_cmd, maxread=10000000)
   except:
      print "INFO: CAN'T START SLIMPRO PROCESS"
      ddrshmoo_system_exit(FA_comments)
   ddr_slimpro_process.delaybeforesend=1
   ddr_dut_process.delaybeforesend=1
   index = 100
   #ddr_slimpro_process.expect(':', timeout=60)
   #ddr_slimpro_process.sendline('amcc1234\r')
   #ddr_dut_process.expect(':', timeout=60)
   #ddr_dut_process.sendline('amcc1234\r')

   if (screen_option == "ddr_only"):
      headerfile(logfile, FA_comments)

   power_cycle=int(ddr_power_cycle_count) 
   print "\n"
   print "="*60
   print "      DDR SHMOO Test with Power Recycling    "
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
      index=ddr_slimpro_process.expect([pexpect.TIMEOUT, 'Boot.*from.*SPI-NOR'], timeout=60)
      if index == 0:
         print "INFO: Slimpro doesn't boot"
         ddrshmoo_system_exit(FA_comments)
      time.sleep(5)
      ddr_slimpro_process.sendline('y\r')
      time.sleep(1)
      print "INFO: SLIMPRO PROCESS IS DONE!"

      index=100
      index=ddr_dut_process.expect([pexpect.TIMEOUT,'cold reset','Mustang#'], timeout=120)
      if index == 0:
         print "INFO: U-boot doesn't boot"
         ddrshmoo_boot_fail = int(1)
         ddrshmoo_system_exit(FA_comments)
      elif index == 1:
         print "INFO: U-boot cold reset"
         ddrshmoo_boot_fail = int(1)
         ddrshmoo_system_exit(FA_comments)
      print "INFO: >>> U-BOOT BOOTED UP SUCCESSFULLY! <<<"
      if qual == int(1):
         ddr_dut_process.sendline('md 0x7E820900; md 0x7E860900; md 0x7E8A0900; md 0x7E8E0900')
         ddr_dut_process.expect('Mustang#')
      time.sleep(1)
      #ddr_dut_process.sendline('tftp 0x001d000000 storm/ddr_shmoo/16060709/ubsa-16060709.bin\r')
      ddr_dut_process.sendline('tftp 0x001d000000 storm/new_blt_release/ubsa.bin\r')
      time.sleep(1)   
      ddr_dut_process.expect('Mustang#')
      time.sleep(1)
      ddr_dut_process.sendline('go 0x1d000000\r')
      index=100
      index=ddr_dut_process.expect([pexpect.TIMEOUT,'ubsa #'], timeout=5)
      if index == 0:
         print "INFO: UBSA doesn't boot"
         ddrshmoo_system_exit(FA_comments)
      print "INFO: UBSA BOOTED UP SUCCESSFULLY!"
      time.sleep(15)
      if DPC == 1:
         ddr_dut_process.sendline(cmd_images_dict['mem_screen_cmd_1dpc'])
      elif DPC == 2:
         ddr_dut_process.sendline(cmd_images_dict['mem_screen_cmd_2dpc'])   
      index = 100
      index=ddr_dut_process.expect([pexpect.TIMEOUT, test_sig_map['ddr_shmoo']['PASS'], test_sig_map['ddr_shmoo']['FAIL']], timeout=600) 
      if (index == 0) or (index == 2):
         test_result_map['ddr_shmoo'] = 'FAIL'
         test_summary_map['ddr_shmoo'] = 'FAIL'
         print bcolors.FAIL + "INFO: DDR SHMOO TEST:",test_result_map['ddr_shmoo'] + bcolors.ENDC
         ddrshmoo_no_test_pass_fail_map['FAIL']+=1
         if qual != 1:
            ddrshmoo_system_exit(FA_comments)
      elif index == 1:
         test_result_map['ddr_shmoo'] = 'PASS'
         if test_summary_map['ddr_shmoo'] == 'FAIL':
            test_summary_map['ddr_shmoo'] = 'FAIL'
         else:
            test_summary_map['ddr_shmoo'] = 'PASS'
         print bcolors.OKGREEN + "INFO: DDR SHMOO TEST:", test_result_map['ddr_shmoo'] + bcolors.ENDC
         ddrshmoo_no_test_pass_fail_map['PASS']+=1 
      else:
         test_result_map['ddr_shmoo'] = 'FAIL'
         test_summary_map['ddr_shmoo'] = 'FAIL'
         print bcolors.FAIL + "INFO: DDR SHMOO TEST:",test_result_map['ddr_shmoo'] + bcolors.ENDC
         ddrshmoo_no_test_pass_fail_map['FAIL']+=1
         ddrshmoo_system_exit(FA_comments)
      if qual == 1 and DPC==1:
         ddr_dut_process.sendline(eye_map['eye_vref_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_vref_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_vref_mcu2'])
         ddr_dut_process.expect('ubsa') 
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_vref_mcu3'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdrise_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdrise_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdrise_mcu2'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdrise_mcu3'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdfall_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdfall_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdfall_mcu2'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdfall_mcu3'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrdq_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrdq_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrdq_mcu2'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrdq_mcu3'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdgate_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdgate_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdgate_mcu2'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_rdgate_mcu3'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrlvl_mcu0'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrlvl_mcu1'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrlvl_mcu2'])
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline('\r')
         ddr_dut_process.expect('ubsa')
         ddr_dut_process.sendline(eye_map['eye_wrlvl_mcu3'])
         ddr_dut_process.expect('ubsa')   
         time.sleep(15)
      m+=1
   ddrshmoo_no_test_pass_fail(logfile)
   print "-"*60
   print "Total No. of DDR SHMOO Pass Test: %s"%ddrshmoo_no_test_pass_fail_map['PASS']
   print "Total No. of DDR SHMOO Fail Test: %s"%ddrshmoo_no_test_pass_fail_map['FAIL']
   print "\n"
   #power_OFF(cfgfile)  #FIX ME.  may need to remove if memtester is running
   ddr_dut_process.close()
   ddr_slimpro_process.close()

   if (test_type == "Screen" and ddrshmoo_no_test_pass_fail_map['FAIL'] == int(1)):
      print "Test exiting..."
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()
