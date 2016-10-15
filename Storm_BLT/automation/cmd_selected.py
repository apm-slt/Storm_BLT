#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : cmd_select.py
Description:
'''

import os
import sys
import re
import time
import pexpect
from vbios_testcase import *
from vbios_test import *
from global_define import *
from bench_info import *
from test_summary import *
from pwrctl_OFF import *
from totaltime import totaltime_taken

def cmd_selected (test_list, dut_process, FA_comments):
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   t_script = ''
   for x in test_list:
      if ((test_type == "Screen" and no_test_pass_fail_map['FAIL'] == int(0)) or test_type == "ES"):
         if test_cmd_map[x] == 'print "exit on fail"':
            t_cmd = test_cmd_map[x]
         elif test_cmd_map[x] == 'go print_ecid\r':
            print "INFO: PRINTING ECID..."
            t_cmd = test_cmd_map[x]
            t_script = print_ecid(dut_process,t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go pcie_lpbk_test 0 2 2 8 2 5\r':
            print "INFO: TESTING PCIE LOOPBACK GEN3..."
            t_cmd = test_cmd_map[x]
            t_script = pcie_gen3_ext_lpbk(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go pcie_lpbk_test 0 2 1 8 2 5\r':
            print "INFO: TESTING PCIE LOOPBACK GEN2..."
            t_cmd = test_cmd_map[x]
            t_script = pcie_gen2_ext_lpbk(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go eth_tx2rx_1g_sata\r':
            print "INFO: TESTING 1G SATA-SGMII TX2RX..."
            t_cmd = test_cmd_map[x]
            t_script = eth_tx2rx_1g_sata(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go eth_tx2rx_1g_xfi\r':
            print "INFO: TESTING 1G XFI-SGMII TX2RX..."
            t_cmd = test_cmd_map[x]
            t_script = eth_tx2rx_1g_xfi(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go link_pcie 0 2 8 15\r':
            print "INFO: TESTING PCIE0/1 LINKUP GEN3..."
            t_cmd = test_cmd_map[x]
            t_script = link_pcie01(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go link_pcie 2 2 1 15\r':
            print "INFO: TESTING PCIE2 LINKUP GEN3..."
            t_cmd = test_cmd_map[x]
            t_script = link_pcie2(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go link_pcie 3 2 8 15\r':
            print "INFO: TESTING PCIE3/4 LINKUP GEN3..."
            t_cmd = test_cmd_map[x]
            t_script = link_pcie34(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go eth_tx2rx_10g':
            print "INFO: TESTING 10G-XFI TX2RX..."
            t_cmd = test_cmd_map[x]
            t_script = eth_tx2rx_10g_xfi(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go sata6_scan\r':
            print "INFO: TESTING SATA 6 PORTS..."
            t_cmd = test_cmd_map[x]
            t_script = sata(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go ebus_test\r':
            print "INFO: TESTING GFC..."
            t_cmd = test_cmd_map[x]
            t_script = gfc(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go slt_set_and_get_date 2014 05 14 17 00 00\r':
            print "INFO: TESTING RTC..."
            t_cmd = test_cmd_map[x]
            t_script = rtc(dut_process, t_cmd, FA_comments)
         elif test_cmd_map[x] == 'go SDIO_test\r':
            print "INFO: TESTING SDIO..."
            t_cmd = test_cmd_map[x]
            t_script = sdio(dut_process, t_cmd, FA_comments) 
         elif test_cmd_map[x] == 'go spi_rw_nand_diff_ratio 4\r': 
            print "INFO: TESTING SPI..."
            t_cmd = test_cmd_map[x]
            t_script = spi(dut_process, t_cmd, FA_comments)        
         elif test_cmd_map[x] == 'go M2B_COPY\r':
            print "INFO: TESTING PACKET DMA..."
            t_cmd = test_cmd_map[x]
            t_script = pdma(dut_process, t_cmd, FA_comments)   
      elif (test_type == "Screen" and no_test_pass_fail_map['FAIL'] == int(1)):
         print "Test exiting..."
         power_OFF(cfgfile)
         test_summary(logfile, ip_list, test_result_map, FA_comments)
         totaltime_taken(logfile)
         sys.exit()
      time.sleep(5)
      t_script   
   if (test_type == "Screen" and no_test_pass_fail_map['FAIL'] == int(1)):
      print "Test exiting..."
      power_OFF(cfgfile)
      test_summary(logfile, ip_list, test_result_map, FA_comments)
      totaltime_taken(logfile)
      sys.exit()   



