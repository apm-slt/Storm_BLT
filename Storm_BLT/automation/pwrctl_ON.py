#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : pwrctl_ON.py
Description:
'''

import os
import sys
import re
import time
from headerfile import *
from bench_info import *
from nps import *

def power_ON(cfgfile):
   cmd = '/on'
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   time.sleep(2)
   print "== POWER ON THE SLT BENCH!!! =="
   MPCPowerCycle(nps, p_port, cmd)
   #time.sleep(2)
