from subprocess import run
import hw_config as cfg
import numpy as np
from power_modeling import power_modeling
from area_modeling import area_modeling


#acc0 = cfg.hwc(config = cfg.Config(bus_width = 256, is_depth = 1024, al = 128, pc = 8, scr = 8, os_depth = 2048))
#gli = ("mvm",(64,1024,1024))

def evaluate(acc0, gli, dataflow):
   types = [
           "Lin", # 0
           "Linp", # 1
           "Lwt", # 2
           "Lwtp", # 3
           "Cmpfis_aor", # 4
           "Cmpfis_tos", # 5
           "Cmpfis_aos", # 6
           "Cmpfis_ptos", # 7
           "Cmpfis_paos", # 8 
           "Cmpfgt_aor", # 9   
           "Cmpfgt_tos", # 10
           "Cmpfgt_aos", # 11
           "Cmpfgt_ptos", # 12
           "Cmpfgt_paos", # 13
           "Cmpfgtp", # 14
           "Lpenalty", # 15
           "Nop", # 16
           "Nop_w_rd", # 17
           "IS_reward", # 18
           "L2_reward", # 19
           "Fussion" # 20
           ]

   metrics = {}

   cmd = "./CIMMA_Compiler/compiler_count "+str(acc0.BusWidth)+" "+str(acc0.AL)+" "+str(acc0.PC)+" "+str(acc0.SCR)+" "+str(acc0.InputSRAMDepth)+" "+str(acc0.OutputSRAMDepth)+" "+str(acc0.freq)+" \""+gli[0]+"\" "+str(gli[1][0])+" "+str(gli[1][1])+" "+str(gli[1][2])+" \""+dataflow+"\""

   cres = run(cmd, capture_output=True, text=True).stdout.split() # attention the print format in .c
   icnt = np.zeros(21)
   if cres[0] != "ERROR":
      for i in range(21):
         icnt[i] = cres[2*i+1]

      metrics['area'] = area_modeling(acc0) # um2

      ##### energy #####
      power = power_modeling(acc0)
      energy = np.zeros((19,8)) # energy on types[0:17], sum on the last row
      for i in range(18):
         energy[i] = power[i] * icnt[i] * 2 # Unit: pJ
      energy[18] = np.sum(energy[0:19],axis=0) # sum
      same_is_addr_saving = power[4][0]*icnt[18]*2  # power{"Cmpfis_aor","fd_is"} * IS_reward
      energy[18,0] = energy[18,0] - same_is_addr_saving
      energy[18,7] = energy[18,7] - same_is_addr_saving
      metrics['energy'] = energy # pJ

      metrics['cycle'] = sum(icnt[0:17])
      if gli[0] == 'proj':
         metrics['op'] = sum(icnt[4:14])*min(acc0.AL, gli[1][1])*min(acc0.PC, gli[1][0])*2
      else:
         #QK phase & PV phase
         metrics['op'] = (sum(icnt[4:14])-icnt[20])*min(acc0.AL, gli[1][1]/gli[1][2])*min(acc0.PC, gli[1][0])*2
         metrics['op'] += (icnt[20])*min(acc0.AL, gli[1][0])*min(acc0.PC, gli[1][1]/gli[1][2])*2
      #metrics['op'] = sum(icnt[4:14])*acc0.AL*acc0.PC*2

      metrics['delay'] = float(metrics['cycle']) * (1000.0/float(acc0.freq)) # Unit: ns
      metrics['ee_L1'] = float(metrics['op']) / metrics['energy'][18,7] # TOPS/W
      metrics['throughput'] = float(metrics['op']) / metrics['delay'] # GOPS
      metrics['ae_L1'] = float(metrics['throughput']) / metrics['area'][7] *1000 # TOPS/mm2

      bit_energy_L2 = 1 #pJ/bit
      metrics['read_bits_L2'] = (sum(icnt[0:4]) + sum(icnt[9:16]) - icnt[19] - icnt[20])*acc0.BusWidth
      metrics['write_bits_L2'] = (sum(icnt[7:9]) + sum(icnt[12:14]) - icnt[20])*acc0.BusWidth
      energy_L2 = (metrics['read_bits_L2'] + metrics["write_bits_L2"])*bit_energy_L2
      metrics['ee_L2'] = metrics['op'] / (metrics['energy'][18,7] + energy_L2)
      metrics['EDP'] = (metrics['energy'][18,7] + energy_L2) * metrics['delay'] / 1e12 # Unit: nJs

      metrics['energy_L2'] = metrics['op']/metrics['ee_L2']

   else:
      pass

   return metrics


if __name__ == "__main__":
   acc0 = cfg.hwc(config = cfg.Config(bus_width = 256, is_depth = 1024, al = 128, pc = 16, scr = 16, os_depth = 2048))
   gli = ("mvm",(64,64,64))

   for dataflow in ["isap","ispp","wsap","wspp"]:
      metrics = evaluate(acc0, gli, dataflow)

      print(metrics['ee_L2'])
      # print(metrics['delay'])
      # print(metrics['read_bits_L2'])
      # print(metrics['write_bits_L2'])
   print(metrics['area'])

   mld = evaluate(acc0, ("mha",(128,768,12)), 'lhd')
   print(mld['ee_L2'])
   print(mld['ee_L1'])
   print(mld['write_bits_L2'])
   print(mld['read_bits_L2'])



# check methods:
# 1. same ops for dataflows
# 2. enough sram: check read/write L2 bits


