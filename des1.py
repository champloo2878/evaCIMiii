import numpy as np
import hw_config as cfg
from compiler import MicroInstructionCompiler
from evaluator import evaluator
import pickle as pk

def reverse_workload(workload):
    rvw = [' ', [0, 0, 0]]
    rvw[0] = workload[0]
    rvw[1][0] = workload[1][2]
    rvw[1][1] = workload[1][1]
    rvw[1][2] = workload[1][0]
    rvw[1] = tuple(rvw[1])
    return rvw


hw_cfg = cfg.Config(bus_width= 256, is_depth= 1024, al= 128, pc= 16, scr= 16, os_depth= 2048)
# hw_cfg = cfg.Config(bus_width= 1024, is_depth= 1024, al= 1024, pc= 128, scr= 32, os_depth= 2048)
acc0 = cfg.hwc(config= hw_cfg)

workload = ['mvm',(1, 1024, 1024)]

print("IS:", acc0.IS_size, "KB")
print("OS:", acc0.OS_size, "KB")
print("CIMs:", acc0.CIM_size, "KB")
print("Weight:", workload[1][0]*workload[1][1]/1024, "KB")
print("Input:", workload[1][1]*workload[1][2]/1024, "KB")

dataflows = ['isap', 'wsap', 'ispp','wspp']

var_name = [
            'Energy_L1',
            'Area_L1', # um2
            'Cycle',
            'op',
            'Delay', # ns
            'Throughput', # GOPS
            'Energy_Efficiency_L1', # Tops/W
            'Area_Efficiency_L1', # TOPS/mm2"
            'Energy_L2'
            ]
eva_res = np.zeros((8, 9))



for i in range(4):
    cf_compiler = MicroInstructionCompiler(hw_cfg, workload, dataflows[i], VERIFY=False)
    cf_compiler.compile()
    eva = evaluator(acc0, "./cflow/"+dataflows[i]+".log")
    eva.evaluate()
    for j in range(len(var_name)):
        eva_res[i][j] = eva.metrics[var_name[j]]

rvw = reverse_workload(workload)
for i in range(4):
    cf_compiler = MicroInstructionCompiler(hw_cfg, rvw, dataflows[i], VERIFY=False)
    cf_compiler.compile()
    eva = evaluator(acc0, "./cflow/"+dataflows[i]+".log")
    eva.evaluate()
    for j in range(len(var_name)):
        eva_res[i+4][j] = eva.metrics[var_name[j]]


with open("eva_res.pk", "wb") as f:
    pk.dump(eva_res, f)

