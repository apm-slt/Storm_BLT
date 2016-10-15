#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : test_L1.py
Description:
'''

import sys
import os

def test_L1(filename):
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
      elif 'pcie_lpbk_gen2_t_cmd' in x:
         pcie_lpbk_gen2_t_cmd=x.split(':')[1].strip()
         test_list.append(pcie_lpbk_gen2_t_cmd)
      elif 'pcie_lpbk_gen3_t_cmd' in x:
         pcie_lpbk_gen3_t_cmd=x.split(':')[1].strip()
         test_list.append(pcie_lpbk_gen3_t_cmd)
      elif 'eth_tx2rx_10g_t_cmd' in x:
         eth_tx2rx_10g_t_cmd=x.split(':')[1].strip()
         test_list.append(eth_tx2rx_10g_t_cmd)
      elif 'sata_t_cmd' in x:
         sata_t_cmd=x.split(':')[1].strip()
         test_list.append(sata_t_cmd)
      elif 'sdio_t_cmd' in x:
         sdio_t_cmd=x.split(':')[1].strip()
         test_list.append(sdio_t_cmd)
      elif 'spi_t_cmd' in x:
         spi_t_cmd=x.split(':')[1].strip()
         test_list.append(spi_t_cmd)
      elif 'gfc_t_cmd' in x:
         gfc_t_cmd=x.split(':')[1].strip()
         test_list.append(gfc_t_cmd)
      elif 'rtc_t_cmd' in x:
         rtc_t_cmd=x.split(':')[1].strip()
         test_list.append(rtc_t_cmd)
      elif 'pdma_t_cmd' in x:
         pdma_t_cmd=x.split(':')[1].strip()
         test_list.append(pdma_t_cmd)

   fd.close()
   return test_list

