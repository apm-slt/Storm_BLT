#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : headerfile.py
Description:
'''

import os
from bench_info import *
from global_define import *
from vbios_testcase import *

def headerfile(filename, FA_comments):
   os.chmod(filename, 777)
   fd=open(filename, 'w')
   [user, ip, nps, vbios_prompt, p_port, DPC, lot_no, build_id, test_type, screen_option, FA, uart_port_ttyS2, uart_port_ttyS3, minicom_cap_slimpro, vbios_power_cycle_count, ddr_power_cycle_count, linux_power_cycle_count]=bench_info(cfgfile)
   print "=====POWERED BY==================================================================================="
   print "XXXXXXX       XXXXXXX                    SSSSSSSSSSSSSSS LLLLLLLLLLL       TTTTTTTTTTTTTTTTTTTTTTT"
   print "X:::::X       X:::::X                  SS:::::::::::::::SL:::::::::L       T:::::::::::::::::::::T"
   print "X:::::X       X:::::X                 S:::::SSSSSS::::::SL:::::::::L       T:::::::::::::::::::::T"
   print "X::::::X     X::::::X                 S:::::S     SSSSSSSLL:::::::LL       T:::::TT:::::::TT:::::T"
   print "XXX:::::X   X:::::XXX                 S:::::S              L:::::L         TTTTTT  T:::::T  TTTTTT"
   print "   X:::::X X:::::X                    S:::::S              L:::::L                 T:::::T"
   print "    X:::::X:::::X                      S::::SSSS           L:::::L                 T:::::T"
   print "     X:::::::::X      ---------------   SS::::::SSSSS      L:::::L                 T:::::T"
   print "     X:::::::::X      -:::::::::::::-     SSS::::::::SS    L:::::L                 T:::::T"
   print "    X:::::X:::::X     ---------------        SSSSSS::::S   L:::::L                 T:::::T"
   print "   X:::::X X:::::X                                S:::::S  L:::::L                 T:::::T"
   print "XXX:::::X   X:::::XXX                             S:::::S  L:::::L         LLLLLL  T:::::T"
   print "X::::::X     X::::::X                 SSSSSSS     S:::::SLL:::::::LLLLLLLLL:::::LTT:::::::TT"
   print "X:::::X       X:::::X                 S::::::SSSSSS:::::SL::::::::::::::::::::::LT:::::::::T"
   print "X:::::X       X:::::X                 S:::::::::::::::SS L::::::::::::::::::::::LT:::::::::T"
   print "XXXXXXX       XXXXXXX                  SSSSSSSSSSSSSSS   LLLLLLLLLLLLLLLLLLLLLLLLTTTTTTTTTTT"
   print "=================================================================================================="
   print "============================ [Bench-%s: SETUP_INFO ] =============================================="%b_num
   print "\n== READ THE SETUP INFORMATION FOR SLT BENCH!!! =="
   print "Operator         =",user
   print "Board IP         =",ip
   print "NPS IP           =",nps
   print "VBIOS Prompt     =",vbios_prompt
   print "NPS Port         =",p_port
   print "DPC              =",DPC
   print "Storm Lot Number =",lot_no
   print "VBIOS Build      =",build_id
   print "Test Type        =",test_type
   print "Screen Option    =",screen_option
   print "FA               =",FA
   print "DUT Uart         =",uart_port_ttyS2
   print "Slimpro Uart     =",uart_port_ttyS3
   print "Slimpro Capfile  =",minicom_cap_slimpro
   print "VBIOS Pwr Cycle  =",vbios_power_cycle_count
   print "DDR Pwr Cycle    =",ddr_power_cycle_count
   print "Linux Pwr Cycle  =",linux_power_cycle_count
   print "Comments         =",FA_comments
   print "="*99

   print >> fd, "=====POWERED BY==================================================================================="
   print >> fd, "XXXXXXX       XXXXXXX                    SSSSSSSSSSSSSSS LLLLLLLLLLL       TTTTTTTTTTTTTTTTTTTTTTT"
   print >> fd, "X:::::X       X:::::X                  SS:::::::::::::::SL:::::::::L       T:::::::::::::::::::::T"
   print >> fd, "X:::::X       X:::::X                 S:::::SSSSSS::::::SL:::::::::L       T:::::::::::::::::::::T"
   print >> fd, "X::::::X     X::::::X                 S:::::S     SSSSSSSLL:::::::LL       T:::::TT:::::::TT:::::T"
   print >> fd, "XXX:::::X   X:::::XXX                 S:::::S              L:::::L         TTTTTT  T:::::T  TTTTTT"
   print >> fd, "   X:::::X X:::::X                    S:::::S              L:::::L                 T:::::T"
   print >> fd, "    X:::::X:::::X                      S::::SSSS           L:::::L                 T:::::T"
   print >> fd, "     X:::::::::X      ---------------   SS::::::SSSSS      L:::::L                 T:::::T"
   print >> fd, "     X:::::::::X      -:::::::::::::-     SSS::::::::SS    L:::::L                 T:::::T"
   print >> fd, "    X:::::X:::::X     ---------------        SSSSSS::::S   L:::::L                 T:::::T"
   print >> fd, "   X:::::X X:::::X                                S:::::S  L:::::L                 T:::::T"
   print >> fd, "XXX:::::X   X:::::XXX                             S:::::S  L:::::L         LLLLLL  T:::::T"
   print >> fd, "X::::::X     X::::::X                 SSSSSSS     S:::::SLL:::::::LLLLLLLLL:::::LTT:::::::TT"
   print >> fd, "X:::::X       X:::::X                 S::::::SSSSSS:::::SL::::::::::::::::::::::LT:::::::::T"
   print >> fd, "X:::::X       X:::::X                 S:::::::::::::::SS L::::::::::::::::::::::LT:::::::::T"
   print >> fd, "XXXXXXX       XXXXXXX                  SSSSSSSSSSSSSSS   LLLLLLLLLLLLLLLLLLLLLLLLTTTTTTTTTTT"
   print >> fd, "=================================================================================================="
   print >> fd, "============================ [Bench-%s: SETUP_INFO ] =============================================="%b_num
   print >> fd, "\n== READ THE SETUP INFORMATION FOR SLT BENCH!!! =="
   print >> fd, "Operator         =",user
   print >> fd, "Board IP         =",ip
   print >> fd, "NPS IP           =",nps
   print >> fd, "VBIOS Prompt     =",vbios_prompt
   print >> fd, "NPS Port         =",p_port
   print >> fd, "DPC              =",DPC
   print >> fd, "Storm Lot Number =",lot_no
   print >> fd, "VBIOS Build      =",build_id
   print >> fd, "Test Type        =",test_type
   print >> fd, "Screen Option    =",screen_option
   print >> fd, "FA               =",FA
   print >> fd, "DUT Uart         =",uart_port_ttyS2
   print >> fd, "Slimpro Uart     =",uart_port_ttyS3
   print >> fd, "Slimpro Capfile  =",minicom_cap_slimpro
   print >> fd, "VBIOS Pwr Cycle  =",vbios_power_cycle_count
   print >> fd, "DDR Pwr Cycle    =",ddr_power_cycle_count
   print >> fd, "Linux Pwr Cycle  =",linux_power_cycle_count
   print >> fd, "Comments         =",FA_comments
   print >> fd, "="*99

   fd.close()
