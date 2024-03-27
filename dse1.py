from sw_decima import Bert_decision
import hw_config as cfg
import numpy as np
import pickle as pk


bus_width_space = [128, 256, 512]
is_depth_space = [32, 128, 256, 512, 1024]
al_space = [64, 128, 256]
pc_space = [8, 16, 32]
scr_space = [8, 16, 32, 64]
os_depth_space = [32, 256, 1024, 2048]

num_point = len(bus_width_space)*len(is_depth_space)*len(al_space)*len(pc_space)*len(scr_space)*len(os_depth_space)
print(num_point)
dse_res = [[0 for i in range(4)] for i in range(num_point)]

for op_target in ['ee_L2','throughput','EDP']: 
    pi = 0
    for bus_width in bus_width_space:
        for is_depth in is_depth_space:
            for al in al_space:
                for pc in pc_space:
                    for scr in scr_space:
                        for os_depth in os_depth_space:

                            acc0 = cfg.hwc(config = cfg.Config(bus_width = bus_width, is_depth = is_depth, al = al, pc = pc, scr = scr, os_depth = os_depth))

                            return_metric, decision, total_area = Bert_decision(acc0, seq_len=64, hidden_size=1024, head_num=16, num_layers=12, op_target=op_target)

                            dse_res[pi][0] = total_area
                            dse_res[pi][1] = return_metric
                            dse_res[pi][2] = decision
                            dse_res[pi][3] = [bus_width, is_depth, al, pc, scr, os_depth]

                            pi += 1
                            print(op_target+".point:", pi)


    with open("bert_large_N64_dse_"+op_target+".pk", "wb") as f:
        pk.dump(dse_res, f)


