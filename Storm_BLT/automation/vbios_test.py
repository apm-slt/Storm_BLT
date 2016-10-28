#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : vbios_test.py
Description:
'''

import os
import sys
import re
import time
import pexpect
import time
from global_define import *
from vbios_system_exit import *
from ecid import *


def print_ecid(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   time.sleep(5)
   ecid0,ecid1,ecid2,ecid3=ecid(logfile)
   if efused_part == 'yes': 
      if ecid0=='0x00000000' or ecid0==int(0) or  ecid1=='0x00000000' or ecid1==int(0) or ecid2==int(0) or ecid2=='0x00000000' or ecid3=='0x00000000' or ecid3==int(0):
         print bcolors.FAIL + "INFO: THIS PART ISN'T EFUSED.  REJECTED!!!!" + bcolors.ENDC
         print('exiting...')
         vbios_system_exit(FA_comments)

def pcie_gen3_ext_lpbk(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['pcie_gen3_ext_lpbk']['PASS'], test_sig_map['pcie_gen3_ext_lpbk']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=120)
   if (index == 0) or (index == 2):
      test_result_map['pcie_gen3_ext_lpbk']= 'FAIL'
      test_summary_map['pcie_gen3_ext_lpbk']= 'FAIL'
      print bcolors.FAIL + "INFO: PCIE EXTERNAL LOOPBACK GEN3:",test_result_map['pcie_gen3_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['pcie_gen3_ext_lpbk'] = 'PASS'
      if test_summary_map['pcie_gen3_ext_lpbk'] == 'FAIL':
         test_summary_map['pcie_gen3_ext_lpbk'] = 'FAIL'
      else:
         test_summary_map['pcie_gen3_ext_lpbk'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PCIE EXTERNAL LOOPBACK GEN3:", test_result_map['pcie_gen3_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['pcie_gen3_ext_lpbk'] = 'FAIL'
      test_summary_map['pcie_gen3_ext_lpbk'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['pcie_gen3_ext_lpbk']= 'FAIL'
      test_summary_map['pcie_gen3_ext_lpbk'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE EXTERNAL LOOPBACK GEN3:",test_result_map['pcie_gen3_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def pcie_gen2_ext_lpbk(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['pcie_gen2_ext_lpbk']['PASS'], test_sig_map['pcie_gen2_ext_lpbk']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=120)
   if (index == 0) or (index == 2):
      test_result_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      test_summary_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE EXTERNAL LOOPBACK GEN2:",test_result_map['pcie_gen2_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['pcie_gen2_ext_lpbk'] = 'PASS'
      if test_summary_map['pcie_gen2_ext_lpbk'] == 'FAIL':
         test_summary_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      else:
         test_summary_map['pcie_gen2_ext_lpbk'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PCIE EXTERNAL LOOPBACK GEN2:", test_result_map['pcie_gen2_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      test_summary_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      test_summary_map['pcie_gen2_ext_lpbk'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE EXTERNAL LOOPBACK GEN2:",test_result_map['pcie_gen2_ext_lpbk'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def eth_tx2rx_1g_sata(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['eth_tx2rx_1g_sata']['PASS'], test_sig_map['eth_tx2rx_1g_sata']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=120)
   if (index == 0) or (index==2):
      test_result_map['eth_tx2rx_1g_sata'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_sata'] = 'FAIL'
      print bcolors.FAIL + "INFO: 1G SATA-SGMII TEST:",test_result_map['eth_tx2rx_1g_sata'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['eth_tx2rx_1g_sata'] = 'PASS'
      if test_summary_map['eth_tx2rx_1g_sata'] == 'FAIL':
         test_summary_map['eth_tx2rx_1g_sata'] = 'FAIL'
      else:
         test_summary_map['eth_tx2rx_1g_sata'] = 'PASS'
      print bcolors.OKGREEN + "INFO: 1G SATA-SGMII TEST:", test_result_map['eth_tx2rx_1g_sata'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['eth_tx2rx_1g_sata'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_sata'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['eth_tx2rx_1g_sata'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_sata'] = 'FAIL'
      print bcolors.FAIL + "INFO: 1G SATA-SGMII TEST:",test_result_map['eth_tx2rx_1g_sata'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def eth_tx2rx_1g_xfi(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['eth_tx2rx_1g_xfi']['PASS'], test_sig_map['eth_tx2rx_1g_xfi']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=120)
   if (index == 0) or (index==2):
      test_result_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO: 1G XFI-SGMII TEST:",test_result_map['eth_tx2rx_1g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['eth_tx2rx_1g_xfi'] = 'PASS'
      if test_summary_map['eth_tx2rx_1g_xfi'] == 'FAIL':
         test_summary_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      else:
         test_summary_map['eth_tx2rx_1g_xfi'] = 'PASS'
      print bcolors.OKGREEN + "INFO: 1G XFI-SGMII TEST:", test_result_map['eth_tx2rx_1g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_1g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO: 1G XFI-SGMII TEST:",test_result_map['eth_tx2rx_1g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def link_pcie01(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['link_pcie01']['PASS'], test_sig_map['link_pcie01']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=60)
   if (index == 0) or (index == 2):
      test_result_map['link_pcie01'] = 'FAIL'
      test_summary_map['link_pcie01'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE0/1 LINK UP GEN3:", test_result_map['link_pcie01'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['link_pcie01'] = 'PASS'
      if test_summary_map['link_pcie01'] == 'FAIL':
         test_summary_map['link_pcie01'] = 'FAIL'
      else:
         test_summary_map['link_pcie01'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PCIE0/1 LINK UP GEN3:", test_result_map['link_pcie01'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['link_pcie01'] = 'FAIL'
      test_summary_map['link_pcie01'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['link_pcie01'] = 'FAIL'
      test_summary_map['link_pcie01'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE0/1 LINK UP GEN3:", test_result_map['link_pcie01'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def link_pcie2(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['link_pcie2']['PASS'], test_sig_map['link_pcie2']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=60)
   if (index == 0) or (index == 2):
      test_result_map['link_pcie2'] = 'FAIL'
      test_summary_map['link_pcie2'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE2 LINK UP GEN3:", test_result_map['link_pcie2'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['link_pcie2'] = 'PASS'
      if test_summary_map['link_pcie2'] == 'FAIL':
         test_summary_map['link_pcie2'] = 'FAIL'
      else:
         test_summary_map['link_pcie2'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PCIE2 LINK UP GEN3:", test_result_map['link_pcie2'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['link_pcie2'] = 'FAIL'
      test_summary_map['link_pcie2'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['link_pcie2'] = 'FAIL'
      test_summary_map['link_pcie2'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE2 LINK UP GEN3:", test_result_map['link_pcie02'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def link_pcie34(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['link_pcie34']['PASS'], test_sig_map['link_pcie34']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=60)
   if (index == 0) or (index == 2):
      test_result_map['link_pcie34'] = 'FAIL'
      test_summary_map['link_pcie34'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE34 LINK UP GEN3:", test_result_map['link_pcie34'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['link_pcie34'] = 'PASS'
      if test_summary_map['link_pcie34'] == 'FAIL':
         test_summary_map['link_pcie34'] = 'FAIL'
      else:
         test_summary_map['link_pcie34'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PCIE3/4 LINK UP GEN3:", test_result_map['link_pcie34'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['link_pcie34'] = 'FAIL'
      test_summary_map['link_pcie34'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['link_pcie34'] = 'FAIL'
      test_summary_map['link_pcie34'] = 'FAIL'
      print bcolors.FAIL + "INFO: PCIE3/4 LINK UP GEN3:", test_result_map['link_pcie34'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def eth_tx2rx_10g_xfi(dut_process, t_cmd, FA_comments):
   dut_process.sendline(t_cmd)
   dut_process.expect([pexpect.TIMEOUT, 'Select Test no. from the above Menu : 0x'], timeout=360)
   time.sleep(10)
   dut_process.sendline('36\r')
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['eth_tx2rx_10g_xfi']['PASS'], test_sig_map['eth_tx2rx_10g_xfi']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=150)
   if (index == 0) or (index == 2):
      test_result_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO: 10G-XFI TEST:",test_result_map['eth_tx2rx_10g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['eth_tx2rx_10g_xfi'] = 'PASS'
      if test_summary_map['eth_tx2rx_10g_xfi'] == 'FAIL':
         test_summary_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      else:
         test_summary_map['eth_tx2rx_10g_xfi'] = 'PASS'
      print bcolors.OKGREEN + "INFO: 10G-XFI TEST:", test_result_map['eth_tx2rx_10g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      test_summary_map['eth_tx2rx_10g_xfi'] = 'FAIL'
      print bcolors.FAIL + "INFO: 10G-XFI TEST:",test_result_map['eth_tx2rx_10g_xfi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def sata(dut_process, t_cmd, FA_comments):
   dut_process.sendline('\r')
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['sata']['PASS'], test_sig_map['sata']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=120)
   if (index == 0) or (index == 2):
      test_result_map['sata'] = 'FAIL'
      test_summary_map['sata'] = 'FAIL'
      print bcolors.FAIL + "INFO: SATA TEST:",test_result_map['sata']  + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['sata']  = 'PASS'
      if test_summary_map['sata']  == 'FAIL':
         test_summary_map['sata']  = 'FAIL'
      else:
         test_summary_map['sata']  = 'PASS'
      print bcolors.OKGREEN + "INFO: SATA TEST:", test_result_map['sata']  + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['sata'] = 'FAIL'
      test_summary_map['sata'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['sata'] = 'FAIL'
      test_summary_map['sata'] = 'FAIL'
      print bcolors.FAIL + "INFO: SATA TEST:",test_result_map['sata']  + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def gfc(dut_process, t_cmd, FA_comments):
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['gfc']['PASS'], test_sig_map['gfc']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=20)
   time.sleep(2)
   dut_process.sendline('\x03')
   if (index == 0) or (index == 2):
      test_result_map['gfc'] = 'FAIL'
      test_summary_map['gfc'] = 'FAIL'
      print bcolors.FAIL + "INFO: GFC TEST:", test_result_map['gfc'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['gfc'] = 'PASS'
      if test_summary_map['gfc'] == 'FAIL':
         test_summary_map['gfc'] = 'FAIL'
      else:
         test_summary_map['gfc'] = 'PASS'
      print bcolors.OKGREEN + "INFO: GFC TEST:", test_result_map['gfc'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['gfc'] = 'FAIL'
      test_summary_map['gfc'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['gfc'] = 'FAIL'
      test_summary_map['gfc'] = 'FAIL'
      print bcolors.FAIL + "INFO: GFC TEST:", test_result_map['gfc'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def sdio(dut_process, t_cmd, FA_comments):
   time.sleep(2)
   dut_process.sendline(t_cmd)
   dut_process.expect([pexpect.TIMEOUT, 'Please enter an integer number between 0 and 5'], timeout=5)
   dut_process.sendline('5\r')
   dut_process.expect([pexpect.TIMEOUT, 'Please enter sector address from 1 to 10000 or press'], timeout=5)
   dut_process.sendline('1000\r')
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['sdio']['PASS'], test_sig_map['sdio']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=30)
   time.sleep(2)
   if (index == 0) or (index == 2):
      test_result_map['sdio'] = 'FAIL'
      test_summary_map['sdio'] = 'FAIL'
      print bcolors.FAIL + "INFO: SDIO TEST:", test_result_map['sdio'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['sdio'] = 'PASS'
      if test_summary_map['sdio'] == 'FAIL':
         test_summary_map['sdio'] = 'FAIL'
      else:
         test_summary_map['sdio'] = 'PASS'
      print bcolors.OKGREEN + "INFO: SDIO TEST:", test_result_map['sdio'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['sdio'] = 'FAIL'
      test_summary_map['sdio'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['sdio'] = 'FAIL'
      test_summary_map['sdio'] = 'FAIL'
      print bcolors.FAIL + "INFO: SDIO TEST:", test_result_map['sdio'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def spi(dut_process, t_cmd, FA_comments):
   time.sleep(2)
   dut_process.sendline(t_cmd)
   dut_process.expect([pexpect.TIMEOUT, 'Please choose speed before running SPI:'], timeout=10)
   time.sleep(1)
   dut_process.sendline('4\r')
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['spi']['PASS'], test_sig_map['spi']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=20)
   time.sleep(2)
   dut_process.sendline('\x03')
   if (index == 0) or (index == 2):
      test_result_map['spi'] = 'FAIL'
      test_summary_map['spi'] = 'FAIL'
      print bcolors.FAIL + "INFO: SPI TEST:", test_result_map['spi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['spi'] = 'PASS'
      if test_summary_map['spi'] == 'FAIL':
         test_summary_map['spi'] = 'FAIL'
      else:
         test_summary_map['spi'] = 'PASS'
      print bcolors.OKGREEN + "INFO: SPI TEST:", test_result_map['spi'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['spi'] = 'FAIL'
      test_summary_map['spi'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['spi'] = 'FAIL'
      test_summary_map['spi'] = 'FAIL'
      print bcolors.FAIL + "INFO: SPI TEST:", test_result_map['spi'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')


def rtc(dut_process, t_cmd, FA_comments):
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['rtc']['PASS'], test_sig_map['rtc']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=45)
   time.sleep(2)
   if (index == 0) or (index == 2):
      test_result_map['rtc'] = 'FAIL'
      test_summary_map['rtc'] = 'FAIL'
      print bcolors.FAIL + "INFO: RTC TEST:", test_result_map['rtc'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['rtc'] = 'PASS'
      if test_summary_map['rtc'] == 'FAIL':
         test_summary_map['rtc'] = 'FAIL'
      else:
         test_summary_map['rtc'] = 'PASS'
      print bcolors.OKGREEN + "INFO: RTC TEST:", test_result_map['rtc'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['rtc'] = 'FAIL'
      test_summary_map['rtc'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['rtc'] = 'FAIL'
      test_summary_map['rtc'] = 'FAIL'
      print bcolors.FAIL + "INFO: RTC TEST:", test_result_map['rtc'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

def pdma(dut_process, t_cmd, FA_comments):
   time.sleep(2)
   dut_process.sendline(t_cmd)
   index = 100
   index=dut_process.expect([pexpect.TIMEOUT, test_sig_map['pdma']['PASS'], test_sig_map['pdma']['FAIL'], 'MCU UNCORRECTABLE ERR'], timeout=20)
   time.sleep(2)
   dut_process.sendline('\x03')
   if (index == 0) or (index == 2):
      test_result_map['pdma'] = 'FAIL'
      test_summary_map['pdma'] = 'FAIL'
      print bcolors.FAIL + "INFO: PACKET DMA TEST:", test_result_map['pdma'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')
   elif index == 1:
      test_result_map['pdma'] = 'PASS'
      if test_summary_map['pdma'] == 'FAIL':
         test_summary_map['pdma'] = 'FAIL'
      else:
         test_summary_map['pdma'] = 'PASS'
      print bcolors.OKGREEN + "INFO: PACKET DMA TEST:", test_result_map['pdma'] + bcolors.ENDC
      no_test_pass_fail_map['PASS']+=1
   elif index == 3:
      test_result_map['pdma'] = 'FAIL'
      test_summary_map['pdma'] = 'FAIL'
      print bcolors.FAIL + "INFO:  MCU UNCORRECTABLE ERROR in VBIOS!" + bcolors.ENDC
      test_result_map['ddr_shmoo'] = 'FAIL'
      test_summary_map['ddr_shmoo'] = 'FAIL'
      vbios_system_exit(FA_comments)
   else:
      test_result_map['pdma'] = 'FAIL'
      test_summary_map['pdma'] = 'FAIL'
      print bcolors.FAIL + "INFO: PACKET DMA TEST:", test_result_map['pdma'] + bcolors.ENDC
      no_test_pass_fail_map['FAIL']+=1
      print('exiting...')

