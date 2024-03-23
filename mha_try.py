import numpy as np
import hw_config as cfg
from compiler import MicroInstructionCompiler
from evaluator import evaluator
import pickle as pk




hw_cfg = cfg.Config(bus_width= 256, is_depth= 1, al= 128, pc= 32, scr= 16, os_depth= 2048)
# hw_cfg = cfg.Config(bus_width= 1024, is_depth= 1024, al= 1024, pc= 128, scr= 32, os_depth= 2048)
acc0 = cfg.hwc(config= hw_cfg)

workload = ['mvm',(256, 64, 2)]

print("IS:", acc0.IS_size, "KB")
print("OS:", acc0.OS_size, "KB")
print("CIMs:", acc0.CIM_size, "KB")
print("Weight:", workload[1][0]*workload[1][1]/1024, "KB")
print("Input:", workload[1][1]*workload[1][2]/1024, "KB")

dataflows = ['wspp']

for i in range(len(dataflows)):
    cf_compiler = MicroInstructionCompiler(hw_cfg, workload, dataflows[i], VERIFY=False)
    cf_compiler.compile()




hw_cfg = cfg.Config(bus_width= 256, is_depth= 1024, al= 128, pc= 32, scr= 16, os_depth= 2048)
# hw_cfg = cfg.Config(bus_width= 1024, is_depth= 1024, al= 1024, pc= 128, scr= 32, os_depth= 2048)
acc0 = cfg.hwc(config= hw_cfg)

workload = ['mvm',(64, 256, 1)]

print("IS:", acc0.IS_size, "KB")
print("OS:", acc0.OS_size, "KB")
print("CIMs:", acc0.CIM_size, "KB")
print("Weight:", workload[1][0]*workload[1][1]/1024, "KB")
print("Input:", workload[1][1]*workload[1][2]/1024, "KB")

dataflows = ['ispp']

for i in range(len(dataflows)):
    cf_compiler = MicroInstructionCompiler(hw_cfg, workload, dataflows[i], VERIFY=False)
    cf_compiler.compile()
