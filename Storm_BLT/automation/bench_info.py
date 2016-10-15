#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : bench_info.py
Description:
'''

import sys
import os
import re

def bench_info(filename):
   fd=open(filename, 'r')
   for x in fd.readlines():
      x=x.rstrip()
      if 'user' in x:
         user=x.split('=')[1].strip()
      elif 'ip' in x:
         ip=x.split('=')[1].strip()
      elif 'nps' in x:
         nps=x.split('=')[1].strip()
      elif 'vbios_prompt' in x:
         vbios_prompt=re.split('=', x)[1].strip()
      elif 'p_port' in x:
         p_port=x.split('=')[1].strip()
      elif 'DPC' in x:
         DPC=int(x.split('=')[1].strip())
      elif 'lot_no' in x:
         lot_no=x.split('=')[1].strip()
      elif 'build_id' in x:
         build_id=x.split('=')[1].strip()
      elif 'test_type' in x:
         test_type=x.split('=')[1].strip()
      elif 'screen_option' in x:
         screen_option=x.split('=')[1].strip()
      elif 'FA' in x:
         FA=x.split('=')[1].strip()
      elif 'uart_port_ttyS2' in x:
         uart_port_ttyS2=x.split('=')[1].strip()
      elif 'uart_port_ttyS3' in x:
         uart_port_ttyS3=x.split('=')[1].strip()
      elif 'minicom_capfile' in x:
         minicom_capfile=x.split('=')[1].strip()
      elif 'minicom_cap_slimpro' in x:
         minicom_cap_slimpro=x.split('=')[1].strip()
      elif 'logfile' in x:
         logfile=x.split('=')[1].strip()
      elif 'vbios_power_cycle_count' in x:
         vbios_power_cycle_count=x.split('=')[1].strip()
      elif 'ddr_power_cycle_count' in x:
         ddr_power_cycle_count=x.split('=')[1].strip()
      elif 'linux_power_cycle_count' in x:
         linux_power_cycle_count=x.split('=')[1].strip()
   fd.close()
   return [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]


