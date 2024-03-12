# cmpfis of same address with the last cmpfis, power of the input sram could be ignored.
import numpy as np
import hw_config as cfg
from power_modeling import get_power
from area_modeling import get_area
from compiler import MicroInstructionCompiler


class evaluator:
    def __init__(self, HW, inst_path):
        self.HW = HW
        self.instruction_set = ['Lin', 'Linp', 'Lwt', 'Lwtp', 'Cmpfis', 'Cmpfgt', 'Cmpfgtp', 'Lpenalty', 'Nop']
        self.inst_path = inst_path
        self.power_si = get_power(HW)
        self.area = get_area(HW)
        self.metrics = {
            # Consumption on L1 Level
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
            'Energy_L1': 0.0,
            'FD_IS': 0.0,
            'FD_REG': 0.0,
            'CM_MACRO': 0.0,
            'CM_REG': 0.0,
            'GD_OS': 0.0,
            'GD_REG':0.0,
            'Top_REG': 0.0, 
            'Area_L1': 0.0, # um2
            'Cycle': 0,
            'op': 0,
            'Delay': 0.0, # ns
            'Throughput': 0.0, # GOPS
            'Energy_Efficiency_L1': 0.0, # Tops/W
            'Area_Efficiency_L1': 0.0, # TOPS/mm2

            # Consumption on L2 Level
            'Read_bits_L2': 0.0, # bit
            'Write_bits_L2': 0.0,
            'Energy_L2': 0.0

        }


    def check_prefetch_read(self, inst, power_src, power_pr):
        if inst == '<os_rd_addr>': return power_src + power_pr
        else: return power_src

    def evaluate(self):
        with open(self.inst_path, 'r') as cflow:
            eva_start = False

            for line in cflow:

                if 'starting compiler' in line:
                    eva_start = True
                    print("**eva launch**")
                    continue

                if eva_start:
                    self.metrics['Cycle'] += 1

                    inst = line.split()
                    if inst == []: continue
                    if inst[0] == self.instruction_set[0]: # Lin
                        self.metrics['Lin'] += self.check_prefetch_read(inst[-2], self.power_si[0][7], self.power_si[17][7])
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 

                    elif inst[0] == self.instruction_set[1]: # Linp
                        self.metrics['Linp'] += self.check_prefetch_read(inst[-2], self.power_si[1][7], self.power_si[17][7])
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 
                         
                    elif inst[0] == self.instruction_set[2]: # Lwt
                        self.metrics['Lwt'] += self.check_prefetch_read(inst[-2], self.power_si[2][7], self.power_si[17][7]) 
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 

                    elif inst[0] == self.instruction_set[3]: # Lwtp
                        self.metrics['Lwtp'] += self.check_prefetch_read(inst[-2], self.power_si[3][7], self.power_si[17][7]) 
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 

                    elif inst[0] == self.instruction_set[4]: # Cmpfis
                        self.metrics['op'] += self.HW.AL * self.HW.PC * 2
                        if inst[5] == '<aor>': 
                            self.metrics['Cmpfis_aor'] += self.check_prefetch_read(inst[-2], self.power_si[4][7], self.power_si[17][7]) 

                        elif inst[5] == '<tos>':
                            self.metrics['Cmpfis_tos'] += self.check_prefetch_read(inst[-2], self.power_si[5][7], self.power_si[17][7]) 

                        elif inst[5] == '<aos>':
                            self.metrics['Cmpfis_aos'] += self.check_prefetch_read(inst[-2], self.power_si[6][7], self.power_si[17][7]) 

                        elif inst[5] == '<ptos>':
                            self.metrics['Cmpfis_ptos'] += self.check_prefetch_read(inst[-2], self.power_si[7][7], self.power_si[17][7]) 

                        elif inst[5] == '<paos>':
                            self.metrics['Cmpfis_paos'] += self.check_prefetch_read(inst[-2], self.power_si[8][7], self.power_si[17][7]) 


                    elif inst[0] == self.instruction_set[5]: # Cmpfgt
                        self.metrics['op'] += self.HW.AL * self.HW.PC * 2
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 
                        
                        if inst[5] == '<aor>': 
                            self.metrics['Cmpfgt_aor'] += self.check_prefetch_read(inst[-2], self.power_si[9][7], self.power_si[17][7]) 

                        elif inst[5] == '<tos>':
                            self.metrics['Cmpfgt_tos'] += self.check_prefetch_read(inst[-2], self.power_si[10][7], self.power_si[17][7]) 

                        elif inst[5] == '<aos>':
                            self.metrics['Cmpfgt_aos'] += self.check_prefetch_read(inst[-2], self.power_si[11][7], self.power_si[17][7]) 

                        elif inst[5] == '<ptos>':
                            self.metrics['Cmpfgt_ptos'] += self.check_prefetch_read(inst[-2], self.power_si[12][7], self.power_si[17][7]) 

                        elif inst[5] == '<paos>':
                            self.metrics['Cmpfgt_paos'] += self.check_prefetch_read(inst[-2], self.power_si[13][7], self.power_si[17][7]) 

                    elif inst[0] == self.instruction_set[6]: # Cmpfgtp
                        self.metrics['Cmpfgtp'] += self.check_prefetch_read(inst[-2], self.power_si[14][7], self.power_si[17][7]) 
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 

                    elif inst[0] == self.instruction_set[7]: # Lpenalty
                        self.metrics['Lpenalty'] += self.check_prefetch_read(inst[1 if len(inst) > 1 else 0], self.power_si[15][7], self.power_si[17][7]) 
                        self.metrics['Read_bits_L2'] += self.HW.BusWidth 

                    elif inst[0] == self.instruction_set[8]: # nop
                        self.metrics['Nop'] += self.check_prefetch_read(inst[1 if len(inst) > 1 else 0], self.power_si[16][7], self.power_si[17][7]) 

            self.metrics['Energy_L1'] = (self.metrics['Lin'] + \
                                        self.metrics['Linp'] + \
                                        self.metrics['Lwt'] + \
                                        self.metrics['Lwtp'] + \
                                        self.metrics['Cmpfis_aor'] + \
                                        self.metrics['Cmpfis_tos'] + \
                                        self.metrics['Cmpfis_aos'] + \
                                        self.metrics['Cmpfis_ptos'] + \
                                        self.metrics['Cmpfis_paos'] + \
                                        self.metrics['Cmpfgt_aor'] + \
                                        self.metrics['Cmpfgt_tos'] + \
                                        self.metrics['Cmpfgt_aos'] + \
                                        self.metrics['Cmpfgt_ptos'] + \
                                        self.metrics['Cmpfgt_paos'] + \
                                        self.metrics['Cmpfgtp'] + \
                                        self.metrics['Lpenalty'] + \
                                        self.metrics['Nop']) * (1000/self.HW.freq) # pJ
            
            self.metrics['FD_IS'] = self.area[0]
            self.metrics['FD_REG'] = self.area[1]
            self.metrics['CM_MACRO'] = self.area[2]
            self.metrics['CM_REG'] = self.area[3]
            self.metrics['GD_OS'] = self.area[4]
            self.metrics['GD_REG'] = self.area[5]
            self.metrics['Top_REG'] = self.area[6]
            self.metrics['Area_L1'] = self.area[7]

            self.metrics['Delay'] = self.metrics['Cycle'] * (1000/self.HW.freq) # Unit: ns        
            self.metrics['Energy_Efficiency_L1'] = self.metrics['op'] / self.metrics['Energy_L1']
            self.metrics['Throughput'] = self.metrics['op'] / self.metrics['Delay']
            self.metrics['Area_Efficiency_L1'] = self.metrics['op'] / self.metrics['Delay'] / self.metrics['Area_L1'] * 1000

            bit_access_energy_L2 = 1 # pJ/bit
            self.metrics['Energy_L2'] = (self.metrics['Read_bits_L2'] + self.metrics['Write_bits_L2']) * bit_access_energy_L2

    def evaprint(self):
        for key,value in self.metrics.items():
            print(key,':\t',value) 


# Example usage:
if __name__ == "__main__":
    config = cfg.Config(al=128, pc=16, scr=16, bus_width=256, is_depth=1024, os_depth=2048)
    # config = cfg.Config(al=128, pc=16, scr=4, bus_width=128, is_depth=2, os_depth=1024)
    gli = ['mvm', (64, 768, 768)]
    data_stream = 'wspp'
    VERIFY = False

    compiler = MicroInstructionCompiler(config, gli, data_stream, VERIFY)
    compiler.compile()

    eesama = evaluator(cfg.hwc(config), "./cflow/"+data_stream+".log")
    eesama.evaluate()
    eesama.evaprint()

    # Additional code to output or work with the compiled instructions


