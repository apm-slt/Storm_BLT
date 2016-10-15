#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : ecid.py
Description:
'''
import time
import os
import sys
from global_define import *
from bench_info import *
import csv

def ecid(logfile):
   ecid0=0.0
   ecid1=0.0
   ecid2=0.0
   ecid3=0.0
   with open(logfile, mode='rb') as fd:
      for line in fd:
         if 'SCU_ECID0' in line:
            list=line.split(':')
            ecid0=list[-1].strip()
         elif 'SCU_ECID1' in line:
            list=line.split(':')
            ecid1=list[-1].strip()
         elif 'SCU_ECID2' in line:
            list=line.split(':')
            ecid2=list[-1].strip()
         elif 'SCU_ECID3' in line:
            list=line.split(':')
            ecid3=list[-1].strip()
      print "ecid0=%s, ecid1=%s, ecid2=%s, ecid3=%s"%(ecid0, ecid1, ecid2, ecid3)
   return ecid0, ecid1, ecid2, ecid3
