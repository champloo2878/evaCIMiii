# cmpfis of same address with the last cmpfis, power of the input sram could be ignored.


import hw_config as cfg
from power_modeling import get_power
import numpy as np

instruction_set = ['Lin', 'Linp', 'Lwt', 'Lwtp', 'Cmpfis', 'Cmpfgt', 'Cmpfgtp', 'Lpenalty', 'Nop']

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
    op = 0
    energy = {
        'Lin': 0.0,
        'Linp': 0.0,
        'Lwt': 0.0,
        'Lwtp': 0.0,
        'Cmpfis_aor': 0.0,
        'Cmpfis_tos': 0.0,
        'Cmpfis_aos': 0.0,
        'Cmpfis_ptos': 0.0,
        'Cmpfis_paos': 0.0,
        'Cmpfgt_aor': 0.0,
        'Cmpfgt_tos': 0.0,
        'Cmpfgt_aos': 0.0,
        'Cmpfgt_ptos': 0.0,
        'Cmpfgt_paos': 0.0,
        'Cmpfgtp': 0.0,
        'Lpenalty': 0.0,
        'Nop': 0.0,
        'Total_Energy_Consump': 0.0
    }
    for line in cflow:

        if 'starting compiler' in line:
            eva_start = True
            print("**eva launch**")
            continue

        if eva_start:
            cycle += 1

            inst = line.split()
            if inst == []: continue
            if inst[0] == instruction_set[0]: # Lin
                energy['Lin'] += check_prefetch_read(inst[-2], power_si[0][7], power_si[17][7]) 

            elif inst[0] == instruction_set[1]: # Linp
                energy['Linp'] += check_prefetch_read(inst[-2], power_si[1][7], power_si[17][7]) 

            elif inst[0] == instruction_set[2]: # Lwt
                energy['Lwt'] += check_prefetch_read(inst[-2], power_si[2][7], power_si[17][7]) 

            elif inst[0] == instruction_set[3]: # Lwtp
                energy['Lwtp'] += check_prefetch_read(inst[-2], power_si[3][7], power_si[17][7]) 

            elif inst[0] == instruction_set[4]: # Cmpfis
                op += acc0.AL * acc0.PC * 2
                if inst[5] == '<aor>': 
                    energy['Cmpfis_aor'] += check_prefetch_read(inst[-2], power_si[4][7], power_si[17][7]) 
                         
                elif inst[5] == '<tos>':
                    energy['Cmpfis_tos'] += check_prefetch_read(inst[-2], power_si[5][7], power_si[17][7]) 

                elif inst[5] == '<aos>':
                    energy['Cmpfis_aos'] += check_prefetch_read(inst[-2], power_si[6][7], power_si[17][7]) 

                elif inst[5] == '<ptos>':
                    energy['Cmpfis_ptos'] += check_prefetch_read(inst[-2], power_si[7][7], power_si[17][7]) 

                elif inst[5] == '<paos>':
                    energy['Cmpfis_paos'] += check_prefetch_read(inst[-2], power_si[8][7], power_si[17][7]) 


            elif inst[0] == instruction_set[5]: # Cmpfgt
                op += acc0.AL * acc0.PC * 2
                if inst[5] == '<aor>': 
                    energy['Cmpfgt_aor'] += check_prefetch_read(inst[-2], power_si[9][7], power_si[17][7]) 

                elif inst[5] == '<tos>':
                    energy['Cmpfgt_tos'] += check_prefetch_read(inst[-2], power_si[10][7], power_si[17][7]) 

                elif inst[5] == '<aos>':
                    energy['Cmpfgt_aos'] += check_prefetch_read(inst[-2], power_si[11][7], power_si[17][7]) 

                elif inst[5] == '<ptos>':
                    energy['Cmpfgt_ptos'] += check_prefetch_read(inst[-2], power_si[12][7], power_si[17][7]) 

                elif inst[5] == '<paos>':
                    energy['Cmpfgt_paos'] += check_prefetch_read(inst[-2], power_si[13][7], power_si[17][7]) 

            elif inst[0] == instruction_set[6]: # Cmpfgtp
                energy['Cmpfgtp'] += check_prefetch_read(inst[-2], power_si[14][7], power_si[17][7]) 

            elif inst[0] == instruction_set[7]: # Lpenalty
                energy['Lpenalty'] += check_prefetch_read(inst[1 if len(inst) > 1 else 0], power_si[15][7], power_si[17][7]) 

            elif inst[0] == instruction_set[8]: # nop
                energy['Nop'] += check_prefetch_read(inst[1 if len(inst) > 1 else 0], power_si[16][7], power_si[17][7]) 

    for key,value in energy.items():
        energy['Total_Energy_Consump'] += value
    energy['Total_Energy_Consump'] = energy['Total_Energy_Consump']/2 * (1000/freq) # Unit: pJ







for key,value in energy.items():
    print(key,':\t',value)

print(cycle)
print(op)

print('Energy_Efficiency:', op / energy['Total_Energy_Consump'], 'TOPS/W')
