#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : pwrctl_OFF.py
Description:
'''

import os
import sys
import re
import time
from bench_info import *
from nps import *
from global_define import *

def power_OFF(cfgfile):
   cmd = '/off'
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   time.sleep(2)
   print "== POWER OFF THE SLT BENCH!!! =="
   MPCPowerCycle(nps, p_port, cmd)
   time.sleep(2)
