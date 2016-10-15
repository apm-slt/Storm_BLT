#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : nps.py
Description:
'''

import pexpect
import os
import sys
import time
import re

def MPCPowerCycle (IpAddr, plug, cmd):
   username='super'
   password='super'
   print IpAddr,plug,cmd
   telnet_process=pexpect.spawn('telnet' + ' ' + IpAddr)
   time.sleep(2)
   telnet_process.expect([pexpect.TIMEOUT,':'], timeout=4)
   time.sleep(2)
   telnet_process.send('super'+'\r')
   telnet_process.expect([pexpect.TIMEOUT,':'], timeout=4)
   telnet_process.send('super'+'\r')
   telnet_process.send('\r\n')
   time.sleep(2)
   telnet_process.expect([pexpect.TIMEOUT,'MPC>'], timeout=4)
   telnet_process.send(cmd+ ' '+ plug + ',' + 'y' + '\r')
   #time.sleep(2)
   #telnet_process.expect([pexpect.TIMEOUT, 'Are you sure? (Y/N):'], timeout=4)
   #telnet_process.send('yes\r')
   time.sleep(2)
   telnet_process.expect([pexpect.TIMEOUT, 'MPC>'], timeout=4)
   telnet_process.send('/x\r')

