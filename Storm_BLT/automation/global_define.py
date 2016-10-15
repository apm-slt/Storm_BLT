#! /usr/bin/python
'''
Author     : Tinh Nguyen
project    : Storm BLT
File       : global_define.py
Description: Depend on which screen PC, consider to change BASE_DIR, CFG_DIR and csv_file
             for 10.76.161.248
'''

import os
import sys
import re
import time
import pexpect

#global define
def get_time():
   #return "%4d%02d%02d%02d%02d%02d"%time.localtime()[:-3]
   return str(time.localtime()[:-3][1]) + '_' + str(time.localtime()[:-3][2]) + '_' + str(time.localtime()[:-3][0]) + '_' \
          + str(time.localtime()[:-3][3]) + '_' + str(time.localtime()[:-3][4]) + '_' + str(time.localtime()[:-3][5])

if len(sys.argv)==1:
   print "INFO: slt_automation.py <test_bench_num>"
   sys.exit()
else:
   b_num = (sys.argv)[-1]

BASE_DIR        = '/home/amcclab'
CFG_DIR         = os.path.join(BASE_DIR, 'Storm_BLT/config')
cfgfile         = os.path.join(CFG_DIR, 'bench_%s.cfg'%b_num)
LOGFILE_DIR     = os.path.join(BASE_DIR, 'logs/Test_Result')
CSV_DIR         = os.path.join(BASE_DIR, 'logs/CSV_FILES')
test_L1_file    = os.path.join(CFG_DIR, 'test_L1.cfg')
test_L_file     = os.path.join(CFG_DIR, 'test_L.cfg')
cmd_images_file = os.path.join(CFG_DIR, 'cmd_images.cfg')
csv_file        = os.path.join(CSV_DIR, 'Storm.csv')

starttime = get_time()
start = time.time()
#logfile = get_time() + '_bench-%s'%b_num + '_SLT_TEST.log'
logfile = 'bench-%s'%b_num + '_slt_' + get_time() + '.log'
print "INFO: Starting SLT Test @time:" + str(starttime)
print "INFO: Logfile:" + logfile
logfile = os.path.join(LOGFILE_DIR, logfile)

test_cmd_map = {'1'                 : 'print "exit on fail"',
                'ecid'              : 'go print_ecid\r',
                'pcie_gen2_ext_lpbk': 'go pcie_lpbk_test 0 2 1 8 2 5\r',
                'pcie_gen3_ext_lpbk': 'go pcie_lpbk_test 0 2 2 8 2 5\r',
                'eth_tx2rx_1g_sata' : 'go eth_tx2rx_1g_sata\r',
                'eth_tx2rx_1g_xfi'  : 'go eth_tx2rx_1g_xfi\r',
                'link_pcie01'       : 'go link_pcie 0 2 8 15\r',
                'link_pcie2'        : 'go link_pcie 2 2 1 15\r',
                'link_pcie34'       : 'go link_pcie 3 2 8 15\r',
                'eth_tx2rx_10g_xfi' : 'go eth_tx2rx_10g',
                'sata'              : 'go sata6_scan\r',
                'gfc'               : 'go ebus_test\r',
                'rtc'               : 'go slt_set_and_get_date 2014 05 14 17 00 00\r',
                'sdio'              : 'go SDIO_test\r',
                'spi'               : 'go spi_rw_nand_diff_ratio 4\r',
                'pdma'               : 'go M2B_COPY\r'
               }


bench_map = {'55': 'test_L',
             '56': 'test_L1'}


test_sig_map = {'pcie_gen3_ext_lpbk':{'PASS': 'Iteration\s4\s<\sPASS\s>\sGen3\sx8',
                                       'FAIL': 'Fail'},
                 'pcie_gen2_ext_lpbk':{'PASS': 'Iteration\s4\s<\sPASS\s>',
                                       'FAIL': 'Fail'},
                 'eth_tx2rx_1g_sata' :{'PASS': 'Test\sResult\s:\sSATA-SGMII\sPASS',
                                       'FAIL': 'Test\sResult\s:\sSATA-SGMII\sFAIL'},
                 'eth_tx2rx_1g_xfi'  :{'PASS': 'Test\sResult\s:\sXFI-SGMII\sPASS',
                                       'FAIL': 'Test\sResult\s:\sXFI-SGMII\sFAIL'},
                 'link_pcie01'       :{'PASS': 'Link\sPASS\sGen3x8\s@\sIteration\sNo.\s= \s15\sRecovery\sCnt=0',
                                       'FAIL': 'FAIL'},
                 'link_pcie2'        :{'PASS': 'Link\sPASS\sGen3x1\s@\sIteration\sNo.\s= \s15\sRecovery\sCnt=0',
                                       'FAIL': 'FAIL'},
                 'link_pcie34'       :{'PASS': 'Link\sPASS\sGen3x8\s@\sIteration\sNo.\s= \s15\sRecovery\sCnt=0',
                                       'FAIL': 'FAIL'},
                 'eth_tx2rx_10g_xfi' :{'PASS': 'Test\sResult\s:\sPASS',
                                       'FAIL': 'Test\sResult\s:\sFAIL'},
                 'sata'              :{'PASS': 'SATA\sScreening\s-\sPass',
                                       'FAIL': 'SATA\sScreening\s-\sFail'},
                 'gfc'               :{'PASS': 'RESULT:\sTEST\sPASS',
                                       'FAIL': 'RESULT:\sTEST\sFAIL'},
                 'rtc'               :{'PASS': 'Date: 2014-05-14 17:00:30',
                                       'FAIL': 'Date: 2014-05-14 17:00:31'},
                 'sdio'              :{'PASS': '\#\#\s+Number of PASSED Tests: 05',
                                       'FAIL': 'RESULT:\sTEST\sFAIL'},
                 'spi'               :{'PASS': 'RESULT:\sTEST\sPASS',
                                       'FAIL': 'RESULT:\sTEST\sFAIL'},
                 'pdma'              :{'PASS': 'RESULT:\sTEST\sPASS',
                                       'FAIL': 'RESULT:\sTEST\sFAIL'},
                 'ddr_shmoo'         :{'PASS': 'mem_screen\stest\sresult\s\(ALL\sranks\):\sPASS',
                                       'FAIL': 'mem_screen\stest\sresult\s\(ALL\sranks\):\sFAIL'},
                 'pmd'               :{'PASS': 'pmd_test: passed: error_status=0',
                                       'FAIL': 'pmd_test: failed'}
                }


test_result_map = {'pcie_gen3_ext_lpbk': 'not tested',
                   'pcie_gen2_ext_lpbk': 'not tested',
                   'eth_tx2rx_1g_sata' : 'not tested',
                   'eth_tx2rx_1g_xfi'  : 'not tested',
                   'link_pcie01'       : 'not tested',
                   'link_pcie2'        : 'not tested',
                   'link_pcie34'       : 'not tested',
                   'eth_tx2rx_10g_xfi' : 'not tested',
                   'sata'              : 'not tested',
                   'gfc'               : 'not tested',
                   'rtc'               : 'not tested',
                   'sdio'              : 'not tested',
                   'spi'               : 'not tested',
                   'pdma'              : 'not tested',
                   'ddr_shmoo'         : 'not tested',
                   'ddr_memtester'     : 'not tested',
                   'linux'             : 'not tested',
                   'pmd'               : 'not tested',
                   'pcie_calib'        : 'not tested'
                   }


test_summary_map = {'pcie_gen3_ext_lpbk': 'not tested',
                    'pcie_gen2_ext_lpbk': 'not tested',
                    'eth_tx2rx_1g_sata' : 'not tested',
                    'eth_tx2rx_1g_xfi'  : 'not tested',
                    'link_pcie01'       : 'not tested',
                    'link_pcie2'        : 'not tested',
                    'link_pcie34'       : 'not tested',
                    'eth_tx2rx_10g_xfi' : 'not tested',
                    'sata'              : 'not tested',
                    'gfc'               : 'not tested',
                    'rtc'               : 'not tested',
                    'spi'               : 'not tested',
                    'pdma'              : 'not tested',
                    'ddr_shmoo'         : 'not tested',
                    'ddr_memtester'     : 'not tested',
                    'sdio'              : 'not tested',
                    'linux'             : 'not tested',
                    'pmd'               : 'not tested',
                    'pcie_calib'        : 'not tested'
                    }


ip_map = {'pcie_gen3_ext_lpbk': 'PCIE EXTERNAL LOOPBACK GEN3',
          'pcie_gen2_ext_lpbk': 'PCIE EXTERNAL LOOPBACK GEN2',
          'eth_tx2rx_1g_sata' : '1G SATA-SGMII TEST',
          'eth_tx2rx_1g_xfi'  : '1G XFI-SGMII TEST',
          'link_pcie01'       : 'PCIE0/1 LINK UP GEN 3',
          'link_pcie2'        : 'PCIE2 LINK UP GEN 3',
          'link_pcie34'       : 'PCIE3/4 LINK UP GEN 3',
          'eth_tx2rx_10g_xfi' : '10G-XFI TEST',
          'sata'              : 'SATA TEST',
          'gfc'               : 'GFC NAND TEST',
          'rtc'               : 'RTC TEST',
          'spi'               : 'SPI TEST',
          'pdma'              : 'PACKET DMA TEST',
          'ddr_shmoo'         : 'DDR SHMOO TEST',
          'ddr_memtester'     : 'DDR MEMTESTER TEST',
          'sdio'              : 'SDIO TEST',
          'linux'             : 'LINUX BOOT TEST',
          'pmd'               : 'PMD TEST',
          'pcie_calib'        : 'PCIE CALIB'
          }


ip_list = ['link_pcie01','link_pcie2','link_pcie34','eth_tx2rx_1g_sata','eth_tx2rx_1g_xfi','pcie_gen3_ext_lpbk','pcie_calib','sata','eth_tx2rx_10g_xfi','spi','gfc','sdio','rtc','pdma','ddr_shmoo','linux','ddr_memtester','pmd']

no_test_pass_fail_map = {'PASS': int(0), 'FAIL': int(0)}
ddrshmoo_no_test_pass_fail_map = {'PASS': int(0), 'FAIL': int(0)}
memtester_no_test_pass_fail_map = {'PASS': int(0), 'FAIL': int(0)}
pmd_no_test_pass_fail_map = {'PASS': int(0), 'FAIL': int(0)}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

list_num_cores=[1,2,3,4,5,6,7]
num_cores=str(8)
mem_value300=300
vbios_boot_fail = int(0)
ddrshmoo_boot_fail = int(0)
memtester_boot_fail = int(0)
pmd_boot_fail = int(0)

test_title_list = ['LOT NO','OPERATOR','BENCH NO','ECID0','ECID1','ECID2','ECID3','PCIE GEN2 LB','SATA','10G-XFI','SPI','GFC','SDIO','RTC', \
                   'PDMA','DDR SHMOO','LINUX','MEMTESTER','PMD','PCIE CALIB','PCIE GEN3 LINK0/1', 'PCIE GEN3 LINK2','PCIE GEN3 LINK3/4','SATA-SGMII', \
                   'XFI-SGMII','DDR SHMOO','LINUX','MEMTESTER','PMD','LOGFILE']


link_pcie_uboot = 1

qual=0

eye_map = {'eye_vref_mcu0': 'eye --with_ecc --lvl vref --lvl_start 0x100 --lvl_end 0x120 --step 1 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_vref_mcu1': 'eye --with_ecc --lvl vref --lvl_start 0x100 --lvl_end 0x120 --step 1 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_vref_mcu2': 'eye --with_ecc --lvl vref --lvl_start 0x100 --lvl_end 0x120 --step 1 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_vref_mcu3': 'eye --with_ecc --lvl vref --lvl_start 0x100 --lvl_end 0x120 --step 1 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdrise_mcu0': 'eye --lvl rdrise --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdrise_mcu1': 'eye --lvl rdrise --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdrise_mcu2': 'eye --lvl rdrise --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdrise_mcu3': 'eye --lvl rdrise --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdfall_mcu0': 'eye --lvl rdfall --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdfall_mcu1': 'eye --lvl rdfall --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdfall_mcu2': 'eye --lvl rdfall --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdfall_mcu3': 'eye --lvl rdfall --lvl_start 0x0 --lvl_end 0x120 --step 4 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrdq_mcu0': 'eye --lvl wrdq --lvl_start 0x1C0 --lvl_end 0x300 --step 4 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrdq_mcu1': 'eye --lvl wrdq --lvl_start 0x1C0 --lvl_end 0x300 --step 4 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrdq_mcu2': 'eye --lvl wrdq --lvl_start 0x1C0 --lvl_end 0x300 --step 4 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrdq_mcu3': 'eye --lvl wrdq --lvl_start 0x1C0 --lvl_end 0x300 --step 4 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw', 
           'eye_rdgate_mcu0': 'eye --lvl rdgate --lvl_start 0x300 --lvl_end 0xC00 --step 20 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdgate_mcu1': 'eye --lvl rdgate --lvl_start 0x300 --lvl_end 0xC00 --step 20 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdgate_mcu2': 'eye --lvl rdgate --lvl_start 0x300 --lvl_end 0xC00 --step 20 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_rdgate_mcu3': 'eye --lvl rdgate --lvl_start 0x300 --lvl_end 0xC00 --step 20 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrlvl_mcu0': 'eye --lvl wrlvl  --lvl_start 0x0 --lvl_end 0x800 --step 20 --mcu 0 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrlvl_mcu1': 'eye --lvl wrlvl  --lvl_start 0x0 --lvl_end 0x800 --step 20 --mcu 1 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrlvl_mcu2': 'eye --lvl wrlvl  --lvl_start 0x0 --lvl_end 0x800 --step 20 --mcu 2 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw',
           'eye_wrlvl_mcu3': 'eye --lvl wrlvl  --lvl_start 0x0 --lvl_end 0x800 --step 20 --mcu 3 -- --threads 8 --iterations 5 --memory 10M --test xor_rmw'
} 

