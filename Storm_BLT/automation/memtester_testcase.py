#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : memtester_testcase.py
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
from memtester_no_test_pass_fail import *
from totaltime import totaltime_taken
from memtester_system_exit import memtester_system_exit
from test_summary import *

def memtester_testcase(FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   cmd_images_dict, cmd_images_list=cmd_images(cmd_images_file)
   ddr_memtester_slimpro_cmd = 'sudo minicom -D ' + uart_port_ttyS3 + ' -C ' + minicom_cap_slimpro
   ddr_memtester_dut_cmd = 'sudo minicom -D ' + uart_port_ttyS2 + ' -C ' + logfile
   os.environ['TERM'] = 'vt100'
   try:
      ddr_memtester_dut_process = pexpect.spawn(ddr_memtester_dut_cmd, maxread=1000000000)
   except:
      print "INFO: CAN'T START DUT PROCESS"
      memtester_system_exit(FA_comments)
   try:
      ddr_memtester_slimpro_process = pexpect.spawn(ddr_memtester_slimpro_cmd, maxread=1000000000)
   except:
      print "INFO: CAN'T START SLIMPRO PROCESS"
      memtester_system_exit(FA_comments)
   ddr_memtester_slimpro_process.delaybeforesend=1
   ddr_memtester_dut_process.delaybeforesend=1

   power_cycle=int(linux_power_cycle_count)
   print "\n"
   print "="*60
   print "      DDR MEMTESTER Test with Power Recycling    "
   print "                                             "
   print "--> No. of power recycles    : ",power_cycle
   print "="*60
   t=0
   ''' test pcie link up in 15 iterations for 2DPC.  If 1DPC, no need to test for pcie linkup in u-boot;however, will 
       test SATA FIO in linux in 1DPC
   '''
   if DPC==2:
      link_pcie_iteration=15
   else:
      link_pcie_iteration=1

   while t<power_cycle:
      print bcolors.OKBLUE +"\n== POWER CYCLE:",int(t+1)," ==" + bcolors.ENDC
      power_OFF(cfgfile)
      time.sleep(5)
      power_ON(cfgfile)
      no_iter=0
      while no_iter < link_pcie_iteration:
         no_iter +=1
         print "PCIE GEN 3 LINKUP ITERATION: %s"%no_iter
         index = 100
         index=ddr_memtester_slimpro_process.expect([pexpect.TIMEOUT, 'Boot.*from.*SPI-NOR'], timeout=60)
         if index == 0:
            print "INFO: Slimpro doesn't boot"
            memtester_system_exit(FA_comments)
         time.sleep(5)   
         ddr_memtester_slimpro_process.sendline('y\r')
         time.sleep(1)
         print "INFO: SLIMPRO PROCESS IS DONE!"
         if link_pcie_uboot == 1 and DPC == 2:
            index01=100
            index01=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, 'PCIE0:.*link.*down','PCIE0:.*X8.*GEN-3.*link.*up', \
            'PCIE0:.*GEN-1.*link.*up','PCIE0:.*GEN-2.*link.*up','PCIE0:.*X4.*link.*up','PCIE0:.*X1.*link.*up'], timeout=200)
            if index01 == 0:
               print "INFO: U-boot doesn't boot"
               memtester_boot_fail = int(1)
               memtester_system_exit(FA_comments)
            elif index01 == 1:
               test_result_map['link_pcie01']= 'FAIL'
               test_summary_map['link_pcie01']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE0/1 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie01'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()
            elif index01 == 2:
               test_result_map['link_pcie01'] = 'PASS'
               if test_summary_map['link_pcie01'] == 'FAIL':
                  test_summary_map['link_pcie01'] = 'FAIL'
               else:
                  test_summary_map['link_pcie01'] = 'PASS'
               print bcolors.OKGREEN + "INFO: PCIE0/1 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie01'] + bcolors.ENDC
            elif index01 >= 3:
               test_result_map['link_pcie01']= 'FAIL'
               test_summary_map['link_pcie01']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE0/1 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie01'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()


            index2=100
            index2=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, 'PCIE2:.*link.*down', 'PCIE2:.*X1.*GEN-3.*link.*up', \
            'PCIE2:.*GEN-1.*link.*up','PCIE2:.*GEN-2.*link.*up'], timeout=200)
            if index2 == 0:
               print "INFO: U-boot doesn't boot"
               memtester_boot_fail = int(1)
               memtester_system_exit(FA_comments)
            elif index2 == 1:
               test_result_map['link_pcie2']= 'FAIL'
               test_summary_map['link_pcie2']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE2 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie2'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()
            elif index2 == 2:
               test_result_map['link_pcie2'] = 'PASS'
               if test_summary_map['link_pcie2'] == 'FAIL':
                  test_summary_map['link_pcie2'] = 'FAIL'
               else:
                  test_summary_map['link_pcie2'] = 'PASS'
               print bcolors.OKGREEN + "INFO: PCIE2 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie2'] + bcolors.ENDC
            elif index2 >= 3:
               test_result_map['link_pcie2']= 'FAIL'
               test_summary_map['link_pcie2']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE2 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie2'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()                       

            index34=100
            index34=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, 'PCIE3:.*link.*down', 'PCIE3:.*X8.*GEN-3.*link.*up', \
            'PCIE3:.*GEN-1.*link.*up','PCIE3:.*GEN-2.*link.*up','PCIE3:.*X4.*link.*up','PCIE3:.*X1.*link.*up'], timeout=200)
            if index34 == 0:
               print "INFO: U-boot doesn't boot"
               memtester_boot_fail = int(1)
               memtester_system_exit(FA_comments)
            elif index34 == 1:
               test_result_map['link_pcie34']= 'FAIL'
               test_summary_map['link_pcie34']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE3/4 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie34'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()
            elif index34 == 2:
               test_result_map['link_pcie34'] = 'PASS'
               if test_summary_map['link_pcie34'] == 'FAIL':
                  test_summary_map['link_pcie34'] = 'FAIL'
               else:
                  test_summary_map['link_pcie34'] = 'PASS'
               print bcolors.OKGREEN + "INFO: PCIE3/4 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie34'] + bcolors.ENDC
            elif index34 >= 3:
               test_result_map['link_pcie34']= 'FAIL'
               test_summary_map['link_pcie34']= 'FAIL'
               print bcolors.FAIL + "INFO: PCIE34 GEN3 LINKUP IN UBOOT:",test_result_map['link_pcie34'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()         
         index=100
         index=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, 'Mustang#'], timeout=120)
         if index == 0:
            print "INFO: U-boot doesn't boot"
            memtester_boot_fail = int(1)
            memtester_system_exit(FA_comments)
         print "INFO: >>> U-BOOT BOOTED UP SUCCESSFULLY! <<<"
         time.sleep(1)
         if no_iter < link_pcie_iteration:
            '''this control how we want to reset the board if need to test for pcie linkup in u-boot'''
            ddr_memtester_dut_process.sendline('reset\r')      

      print "INFO: LINUX Booting..."      
      ddr_memtester_dut_process.sendline('run net_self\r')
      time.sleep(1)
      index=100
      index=ddr_memtester_dut_process.expect([pexpect.TIMEOUT,'login:','SError','Dispar','BadCRC','ATA bus error','Internal error: Oops:','correctable error','uncorrectable error','self-detected stall on CPU','memory error','data error','error occurs','ECC error'], timeout=360)
      if index == 0:
         print "INFO: LINUX doesn't boot"
         test_result_map['linux'] = 'FAIL'
         test_summary_map['linux'] = 'FAIL'
         print bcolors.FAIL + "INFO: LINUX BOOT:",test_result_map['linux'] + bcolors.ENDC
         memtester_system_exit(FA_comments)
      elif index == 1:
         print "INFO: LINUX BOOTED UP SUCCESSFULLY!"
         test_result_map['linux'] = 'PASS'
         test_summary_map['linux'] = 'PASS'
         print bcolors.OKGREEN + "INFO: LINUX BOOT:",test_result_map['linux'] + bcolors.ENDC
      elif index == 2 or index == 3 or index == 4 or index == 5:
         test_result_map['sata'] = 'FAIL'
         test_summary_map['sata'] = 'FAIL'
         print bcolors.FAIL + "INFO: SATA INITIALIZATION:",test_result_map['sata'] + bcolors.ENDC
         power_OFF(cfgfile)
         test_summary(logfile, ip_list, test_result_map, FA_comments)
         totaltime_taken(logfile)
         sys.exit()
      else:
         print "INFO: LINUX NOT BOOTED UP SUCCESSFULLY!"
         test_result_map['linux'] = 'FAIL'
         test_summary_map['linux'] = 'FAIL'
         print bcolors.FAIL + "INFO: LINUX BOOT:",test_result_map['linux'] + bcolors.ENDC
         memtester_system_exit(FA_comments)
         
      time.sleep(1)
      ddr_memtester_dut_process.send('root\r')
      ddr_memtester_dut_process.expect('Password:')
      ddr_memtester_dut_process.send('root\r')
      time.sleep(3)
      
      '''test SATA FIO in LINUX in 1DPC'''
      if DPC == 1:
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sda &\r')  
         time.sleep(1)
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sdb &\r')  
         time.sleep(1)
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sdc &\r')
         time.sleep(1)
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sdd &\r') 
         time.sleep(1)
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sde &\r')
         time.sleep(1)
         ddr_memtester_dut_process.sendline('fio --direct=1 --rw=rw --bs=64k --iodepth=8 --ioengine=libaio --numjobs=1 \
                                           --runtime=300 --time_based --name=/dev/sdf\r') 
         time.sleep(1)
         index = 100
         index=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, '[5].*Done', 'SError', 'QUEUED', 'Error', 'error', \
                                           'FPDMA','UnrecovData', 'Dispar','BadCRC','ATA bus error'], timeout=800)
         if (index >= 2): 
            print "INFO: SATA TEST ERRORS"
            test_result_map['sata'] = 'FAIL'
            test_summary_map['sata'] = 'FAIL'
            print bcolors.FAIL + "INFO: SATA TEST:",test_result_map['sata'] + bcolors.ENDC
            power_OFF(cfgfile)
            test_summary(logfile, ip_list, test_result_map, FA_comments)
            totaltime_taken(logfile)
            sys.exit()
         elif (index==1):
            print "INFO: SATA TEST DONE"
            if test_result_map['sata'] == 'FAIL':
               test_result_map['sata'] = 'FAIL'
               test_summary_map['sata'] = 'FAIL'
               print bcolors.FAIL + "INFO: SATA TEST IN LINUX:",test_result_map['sata'] + bcolors.ENDC
               power_OFF(cfgfile)
               test_summary(logfile, ip_list, test_result_map, FA_comments)
               totaltime_taken(logfile)
               sys.exit()
            elif test_result_map['sata'] != 'FAIL' and test_summary_map['sata'] != 'FAIL':
               test_result_map['sata'] = 'PASS'
               test_summary_map['sata'] = 'PASS'
               print bcolors.OKGREEN + "INFO: SATA TEST IN LINUX:",test_result_map['sata'] + bcolors.ENDC
            elif test_result_map['sata'] != 'FAIL' and test_summary_map['sata'] == 'FAIL':
               test_result_map['sata'] = 'PASS'
               test_summary_map['sata'] = 'FAIL'
               print bcolors.OKGREEN + "INFO: SATA TEST IN LINUX:",test_result_map['sata'] + bcolors.ENDC
         elif (index==0):
            print "SATA TEST TIMEOUT"
            test_result_map['sata'] = 'FAIL'
            test_summary_map['sata'] = 'FAIL'
            print bcolors.FAIL + "INFO: SATA TEST IN LINUX:",test_result_map['sata'] + bcolors.ENDC
            power_OFF(cfgfile)
            test_summary(logfile, ip_list, test_result_map, FA_comments)
            totaltime_taken(logfile)
            sys.exit()
      
      print "INFO: MEMTESTER TESTING..."
      ddr_memtester_dut_process.sendline('echo 0 > /proc/errctl/disable_ce\r')
      time.sleep(3)
      ddr_memtester_dut_process.sendline('export MEMTESTER_TEST_MASK=0x6400\r')
      time.sleep(3)
      for i in [1]:
         for i in list_num_cores:
            ddr_memtester_dut_process.sendline("memtester {}M 1 > /dev/null && echo $? >> temp0.txt &\r".format(mem_value300))
         time.sleep(5)
         ddr_memtester_dut_process.sendline("memtester {}M 1 && echo $? >> temp0.txt\r".format(mem_value300))
         time.sleep(5)
         index=100
         index=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, 'Done', 'ECC', 'FAILURE', 'Error', 'error', 'SError', 'uncorrectable', 'correctable'], timeout=1500)
         if (index==0) or (index==2) or (index==3) or (index==4) or (index==5) or (index==6) or (index==7) or (index==8):
            print "INFO: MEMTEST ERRORS"
            test_result_map['ddr_memtester'] = 'FAIL'
            test_summary_map['ddr_memtester'] = 'FAIL'
            print bcolors.FAIL + "INFO: MEMTESTER TEST:",test_result_map['ddr_memtester'] + bcolors.ENDC
            memtester_no_test_pass_fail_map['FAIL']+=1
            memtester_system_exit(FA_comments)
         elif (index == 1):
            print "INFO: MEMTEST DONE!"
         time.sleep(10)
         ddr_memtester_dut_process.sendline('grep -c {} temp0.txt\r'.format(int(0)))
         index=100
         index=ddr_memtester_dut_process.expect([pexpect.TIMEOUT, num_cores], timeout=60)
         if index == 0:
            test_result_map['ddr_memtester'] = 'FAIL'
            test_summary_map['ddr_memtester'] = 'FAIL'
            print bcolors.FAIL + "INFO: MEMTESTER TEST:",test_result_map['ddr_memtester'] + bcolors.ENDC
            memtester_no_test_pass_fail_map['FAIL']+=1
            memtester_system_exit(FA_comments)
         else:
            test_result_map['ddr_memtester'] = 'PASS'
            if test_summary_map['ddr_memtester'] == 'FAIL':
               test_summary_map['ddr_memtester'] = 'FAIL'
            else:
               test_summary_map['ddr_memtester'] = 'PASS'

            print bcolors.OKGREEN + "INFO: MEMTESTER TEST:",test_result_map['ddr_memtester'] + bcolors.ENDC
            memtester_no_test_pass_fail_map['PASS']+=1
      t+=1
   memtester_no_test_pass_fail(logfile)
   print "-"*60
   print "Total No. of DDR MEMTESTER Pass Test: %s"%memtester_no_test_pass_fail_map['PASS']
   print "Total No. of DDR MEMTESTER Fail Test: %s"%memtester_no_test_pass_fail_map['FAIL']
   print "\n"   
   power_OFF(cfgfile)
   if (test_type == "Screen" and (memtester_no_test_pass_fail_map['FAIL'] == int(1) or test_result_map['sata'] == 'FAIL')):
      print "Test exiting..."
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()


