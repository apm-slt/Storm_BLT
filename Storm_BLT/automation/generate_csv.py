#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : generate_csv.py
Description:
'''


import time
import os
import sys
from global_define import *
from bench_info import *
from ecid import *
import csv
import paramiko

def generate_csv(filename,bench_no,FA_comments='No Label'):
   remote_filename = filename.split('/')[-1]
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   ecid0,ecid1,ecid2,ecid3=ecid(logfile)
   test_summary_list = []
   if DPC == 1:
      test_summary_list = [lot_no,user,bench_no,ecid0,ecid1,ecid2,ecid3,test_summary_map['pcie_gen3_ext_lpbk'], \
      test_summary_map['sata'],test_summary_map['eth_tx2rx_10g_xfi'],test_summary_map['spi'], \
      test_summary_map['gfc'],test_summary_map['sdio'],test_summary_map['rtc'], test_summary_map['pdma'],\
      test_summary_map['ddr_shmoo'],test_summary_map['linux'],test_summary_map['ddr_memtester'],test_summary_map['pmd'], \
      test_summary_map['pcie_calib'],'','', '','','','','','','',remote_filename]
      print test_summary_list
   elif DPC == 2:
      test_summary_list = [lot_no,user,bench_no,ecid0,ecid1,ecid2,ecid3,'','','','','','','','','','','','','',test_summary_map['link_pcie01'], \
      test_summary_map['link_pcie2'],test_summary_map['link_pcie34'],test_summary_map['eth_tx2rx_1g_sata'],test_summary_map['eth_tx2rx_1g_xfi'], \
      test_summary_map['ddr_shmoo'],test_summary_map['linux'],test_summary_map['ddr_memtester'],test_summary_map['pmd'],remote_filename]
      print test_summary_list
   if ip != '192.168.2.102':
      '''access the csv file remotely'''
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      try:
         ssh.connect('192.168.2.102', username='user', password='1Password1')
         sftp_client = ssh.open_sftp()
         sftp_client.chdir("/home/user/LogFiles/Storm_LogFiles/Production_Log/CSV_FILES")

         '''create/write or append existing csv file'''
         try:
            print(sftp_client.stat('Storm_LotNo_%s.csv'%lot_no))
            print('INFO: Writing test results into Database ...')
            fh=sftp_client.open('Storm_LotNo_%s.csv'%lot_no, mode='a')
            writer=csv.writer(fh)
            writer.writerow(test_summary_list)
            fh.close()
         except IOError:
            print('INFO: Database not exit, create one ...')
            fh=sftp_client.open('Storm_LotNo_%s.csv'%lot_no, mode='w')
            writer=csv.writer(fh)
            writer.writerow(test_title_list)
            writer.writerow(test_summary_list)
            fh.close()
         '''Copy logfile to database'''
         try:
            sftp_client.chdir("/home/user/LogFiles/Storm_LogFiles/Production_Log/Lot_No_%s"%lot_no)
         except IOError:
            sftp_client.mkdir("/home/user/LogFiles/Storm_LogFiles/Production_Log/Lot_No_%s"%lot_no)
         sftp_client.chdir("/home/user/LogFiles/Storm_LogFiles/Production_Log/Lot_No_%s"%lot_no)
         print('INFO: Copy logfile to Database...')
         sftp_client.put(filename, './%s'%remote_filename)
         sftp_client.close()
         ssh.close()
      except paramiko.SSHException:
         print("ERROR: >>>> Connection Error <<<<")
         

