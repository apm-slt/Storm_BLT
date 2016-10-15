#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : cmd_images.py
Description:
'''
import sys
import os

def cmd_images(filename):
   cmd_images_dict={}
   cmd_images_list=[]
   fd=open(filename, 'r')
   for x in fd.readlines():
      x=x.rstrip()
      if 'linux_binary' in x:
         linux_binary=x.split('=')[1].strip()
         cmd_images_list.append(linux_binary)
         cmd_images_dict.update({'linux_binary': linux_binary})
      elif 'ddr_shmoo_binary' in x:
         ddr_shmoo_binary=x.split('=')[1].strip()
         cmd_images_list.append(ddr_shmoo_binary)
         cmd_images_dict.update({'ddr_shmoo_binary': ddr_shmoo_binary})
      elif 'pmd_test_binary' in x:
         pmd_test_binary=x.split('=')[1].strip()
         cmd_images_list.append(pmd_test_binary)
         cmd_images_dict.update({'pmd_test_binary': pmd_test_binary})
      elif 'pmd_cmd' in x:
         pmd_cmd=x.split('=')[1].strip()
         cmd_images_list.append(pmd_cmd)
         cmd_images_dict.update({'pmd_cmd': pmd_cmd})
      elif 'no_thread' in x:
         no_thread=x.split('=')[1].strip()
         cmd_images_list.append(no_thread)
         cmd_images_dict.update({'no_thread': no_thread})
      elif 'mem_screen_cmd_1dpc' in x:
         mem_screen_cmd_1dpc=x.split('=')[1].strip()
         cmd_images_list.append(mem_screen_cmd_1dpc)
         cmd_images_dict.update({'mem_screen_cmd_1dpc':  mem_screen_cmd_1dpc})
      elif 'mem_screen_cmd_2dpc' in x:
         mem_screen_cmd_2dpc=x.split('=')[1].strip()
         cmd_images_list.append(mem_screen_cmd_2dpc)
         cmd_images_dict.update({'mem_screen_cmd_2dpc':  mem_screen_cmd_2dpc})
   return cmd_images_dict, cmd_images_list
   fd.close()

