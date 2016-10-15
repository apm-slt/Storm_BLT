#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : test_L.py
Description:
'''

import sys
import os

def test_L(filename):
   test_list=[]
   fd=open(filename, 'r')
   for x in fd.readlines():
      x=x.rstrip()
      if 'blt' in x:
         blt=x.split(':')[1].strip()
         test_list.append(blt)
      elif 'ecid_t_cmd' in x:
         ecid_t_cmd=x.split(':')[1].strip()
         test_list.append(ecid_t_cmd)
      elif 'link_pcie01_t_cmd' in x:
         link_pcie01_t_cmd=x.split(':')[1].strip()
         test_list.append(link_pcie01_t_cmd)
      elif 'link_pcie2_t_cmd' in x:
         link_pcie2_t_cmd=x.split(':')[1].strip()
         test_list.append(link_pcie2_t_cmd)
      elif 'link_pcie34_t_cmd' in x:
         link_pcie34_t_cmd=x.split(':')[1].strip()
         test_list.append(link_pcie34_t_cmd)
      elif 'eth_tx2rx_1g_sata_t_cmd' in x:
         eth_tx2rx_1g_sata_t_cmd=x.split(':')[1].strip()
         test_list.append(eth_tx2rx_1g_sata_t_cmd)
      elif 'eth_tx2rx_1g_xfi_t_cmd' in x:
         eth_tx2rx_1g_xfi_t_cmd=x.split(':')[1].strip()
         test_list.append(eth_tx2rx_1g_xfi_t_cmd)
   fd.close()
   return test_list
