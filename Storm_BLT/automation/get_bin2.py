import re
import sys
from global_define import *

def getvolt(mystr):
  v = 0.77 + int(''.join(list(mystr)[-2:]), 16)/1000.
  return int(v*100)

def binvolt(v):
   vn = int(v)
   if vn >= 97:
      print "BIN_1"
   elif vn >= 95:
      print "BIN_2"
   elif vn >= 94:
      print "BIN_3"
   elif vn >= 93:
      print "BIN_4"
   elif vn >= 86:
      print "BIN_5"
   else:
      print "BIN_6"
   return vn

def get_bin2(filename):
   fd  = open(filename, 'r').readlines()
   val = ""
   for line  in fd:
      if re.search(r'SCU_JTAG1\s+:\s+(\S+)', line):
         tmp2 = re.search(r'SCU_JTAG1\s+:\s+(\S+)', line).groups()
         val = tmp2[0]
         break

   binvolt(getvolt(val))
   #bin_print(filename, vn)
'''
def bin_print(filename, vn):
   fd  = open(filename, 'a')
   if vn >= 97:
      print >> fd, "BIN_1"
   elif vn >= 95:
      print >> fd, "BIN_2"
   elif vn >= 94:
      print >> fd, "BIN_3"
   elif vn >= 93:
      print >> fd, "BIN_4"
   elif vn >= 86:
      print >> fd, "BIN_5"
   else:
      print >> fd, "BIN_6"
'''   
