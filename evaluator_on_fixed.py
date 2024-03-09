# cmpfis of same address with the last cmpfis, power of the input sram could be ignored.


import hw_config as cfg
from power_modeling import get_power
import numpy as np

instruction_set = ['lis', 'lis_p', 'wu', 'wu_p', 'cmpfis', 'cmpgt', 'cmpgtp', 'pload', 'nop']

acc0 = cfg.hwc(config= cfg.Config(bus_width= 256, is_depth= 1024, al= 128, pc= 16, scr= 16, os_depth= 2048))
power_si = get_power(acc0)


inst_path = "./mi.log"
freq = 250 # MHz

def check_prefetch_read(inst, power_src, power_pr):
    if inst == '<os_rd_addr>': return power_src + power_pr
    else: return power_src


with open(inst_path, 'r') as cflow:
    eva_start = False
    cycle = 0
    energy = np.zeros(17)
    for line in cflow:

        if 'starting compiler' in line:
            eva_start = True
            print("**eva launch**")
            continue

        if eva_start:
            cycle += 1

            inst = line.split()
            if inst[0] == instruction_set[0]: # Lin
                energy[0] += check_prefetch_read(inst[-2], power_si[0][7], power_si[17][7]) 

            elif inst[0] == instruction_set[1]: # Linp
                energy[1] += power_si[1][7] 

            elif inst[0] == instruction_set[2]: # Lwt
                energy[2] += power_si[2][7]

            elif inst[0] == instruction_set[3]: # Lwtp
                energy[3] += power_si[3][7] 

            elif inst[0] == instruction_set[4]: # Cmpfis
                if inst[5] == '<aor>': 
                    energy[4] += power_si[4][7]
                         
                elif inst[5] == '<tos>':
                    energy += power_si[5][7]

                elif inst[5] == '<aos>':
                    energy += power_si[6][7]

                elif inst[5] == '<ptos>':
                    energy += power_si[7][7]

                elif inst[5] == '<paos>':
                    energy += power_si[8][7]

            elif inst[0] == instruction_set[5]: # Cmpfgt
                if inst[5] == '<aor>': 
                    energy += power_si[9][7]

                elif inst[5] == '<tos>':
                    energy += power_si[10][7]

                elif inst[5] == '<aos>':
                    energy += power_si[11][7]

                elif inst[5] == '<ptos>':
                    energy += power_si[12][7]

                elif inst[5] == '<paos>':
                    energy += power_si[13][7]

            elif inst[0] == instruction_set[6]: # Cmpfgtp
                    energy += power_si[14][7]

            elif inst[0] == instruction_set[7]: # Lpenalty
                    energy += power_si[15][7]

            elif inst[0] == instruction_set[8]: # nop
                    energy += power_si[16][7] 







        
        if cycle == 50:
            break




