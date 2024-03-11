# cmpfis of same address with the last cmpfis, power of the input sram could be ignored.
import numpy as np
import hw_config as cfg
from power_modeling import get_power
from area_modeling import get_area
from compiler import MicroInstructionCompiler


def check_prefetch_read(inst, power_src, power_pr):
    if inst == '<os_rd_addr>': return power_src + power_pr
    else: return power_src


def evaluator(inst_path, HW):
    instruction_set = ['Lin', 'Linp', 'Lwt', 'Lwtp', 'Cmpfis', 'Cmpfgt', 'Cmpfgtp', 'Lpenalty', 'Nop']
    power_si = get_power(HW)
    area = get_area(HW)
    metrics = {
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
        'Total_energy_Consump': 0.0,
        'Cycle': 0,
        'op': 0,
        'Area': 0.0, # um2
        'Energy_Efficiency': 0.0, # Tops/W
        'Delay': 0.0, # ns
        'Throughput': 0.0, # GOPS
        'Area_Efficiency': 0.0 # TOPS/mm2
    }
    with open(inst_path, 'r') as cflow:
        eva_start = False

        for line in cflow:

            if 'starting compiler' in line:
                eva_start = True
                print("**eva launch**")
                continue

            if eva_start:
                metrics['Cycle'] += 1

                inst = line.split()
                if inst == []: continue
                if inst[0] == instruction_set[0]: # Lin
                    metrics['Lin'] += check_prefetch_read(inst[-2], power_si[0][7], power_si[17][7]) 

                elif inst[0] == instruction_set[1]: # Linp
                    metrics['Linp'] += check_prefetch_read(inst[-2], power_si[1][7], power_si[17][7]) 

                elif inst[0] == instruction_set[2]: # Lwt
                    metrics['Lwt'] += check_prefetch_read(inst[-2], power_si[2][7], power_si[17][7]) 

                elif inst[0] == instruction_set[3]: # Lwtp
                    metrics['Lwtp'] += check_prefetch_read(inst[-2], power_si[3][7], power_si[17][7]) 

                elif inst[0] == instruction_set[4]: # Cmpfis
                    metrics['op'] += HW.AL * HW.PC * 2
                    if inst[5] == '<aor>': 
                        metrics['Cmpfis_aor'] += check_prefetch_read(inst[-2], power_si[4][7], power_si[17][7]) 

                    elif inst[5] == '<tos>':
                        metrics['Cmpfis_tos'] += check_prefetch_read(inst[-2], power_si[5][7], power_si[17][7]) 

                    elif inst[5] == '<aos>':
                        metrics['Cmpfis_aos'] += check_prefetch_read(inst[-2], power_si[6][7], power_si[17][7]) 

                    elif inst[5] == '<ptos>':
                        metrics['Cmpfis_ptos'] += check_prefetch_read(inst[-2], power_si[7][7], power_si[17][7]) 

                    elif inst[5] == '<paos>':
                        metrics['Cmpfis_paos'] += check_prefetch_read(inst[-2], power_si[8][7], power_si[17][7]) 


                elif inst[0] == instruction_set[5]: # Cmpfgt
                    metrics['op'] += HW.AL * HW.PC * 2
                    if inst[5] == '<aor>': 
                        metrics['Cmpfgt_aor'] += check_prefetch_read(inst[-2], power_si[9][7], power_si[17][7]) 

                    elif inst[5] == '<tos>':
                        metrics['Cmpfgt_tos'] += check_prefetch_read(inst[-2], power_si[10][7], power_si[17][7]) 

                    elif inst[5] == '<aos>':
                        metrics['Cmpfgt_aos'] += check_prefetch_read(inst[-2], power_si[11][7], power_si[17][7]) 

                    elif inst[5] == '<ptos>':
                        metrics['Cmpfgt_ptos'] += check_prefetch_read(inst[-2], power_si[12][7], power_si[17][7]) 

                    elif inst[5] == '<paos>':
                        metrics['Cmpfgt_paos'] += check_prefetch_read(inst[-2], power_si[13][7], power_si[17][7]) 

                elif inst[0] == instruction_set[6]: # Cmpfgtp
                    metrics['Cmpfgtp'] += check_prefetch_read(inst[-2], power_si[14][7], power_si[17][7]) 

                elif inst[0] == instruction_set[7]: # Lpenalty
                    metrics['Lpenalty'] += check_prefetch_read(inst[1 if len(inst) > 1 else 0], power_si[15][7], power_si[17][7]) 

                elif inst[0] == instruction_set[8]: # nop
                    metrics['Nop'] += check_prefetch_read(inst[1 if len(inst) > 1 else 0], power_si[16][7], power_si[17][7]) 

        metrics['Total_energy_Consump'] = (metrics['Lin'] + \
                                    metrics['Linp'] + \
                                    metrics['Lwt'] + \
                                    metrics['Lwtp'] + \
                                    metrics['Cmpfis_aor'] + \
                                    metrics['Cmpfis_tos'] + \
                                    metrics['Cmpfis_aos'] + \
                                    metrics['Cmpfis_ptos'] + \
                                    metrics['Cmpfis_paos'] + \
                                    metrics['Cmpfgt_aor'] + \
                                    metrics['Cmpfgt_tos'] + \
                                    metrics['Cmpfgt_aos'] + \
                                    metrics['Cmpfgt_ptos'] + \
                                    metrics['Cmpfgt_paos'] + \
                                    metrics['Cmpfgtp'] + \
                                    metrics['Lpenalty'] + \
                                    metrics['Nop']) * (1000/HW.freq) # pJ

        metrics['Delay'] = metrics['Cycle'] * (1000/HW.freq) # Unit: ns        
        metrics['Area'] = area
        metrics['Energy_Efficiency'] = metrics['op'] / metrics['Total_energy_Consump']
        metrics['Throughput'] = metrics['op'] / metrics['Delay']
        metrics['Area_Efficiency'] = metrics['op'] / metrics['Delay'] / metrics['Area'][7] * 1000

        return metrics

hw_cfg = cfg.Config(bus_width= 256, is_depth= 1024, al= 128, pc= 16, scr= 16, os_depth= 2048)
acc0 = cfg.hwc(config= hw_cfg)

workload = ['mvm',(64, 768, 768)]
dataflow = 'wsap'
cf_compiler = MicroInstructionCompiler(hw_cfg, workload, dataflow, VERIFY=False)
cf_compiler.compile()

metrics = evaluator("./cflow/"+dataflow+".log", acc0)



for key,value in metrics.items():
    print(key,':\t',value)


print('Energy Efficiency:', metrics['Energy_Efficiency'], 'TOPS/W')
print('Throughput:', metrics['Throughput'], 'GOPS')
print('Area Efficiency:', metrics['Area_Efficiency'], 'TOPS/mm2')