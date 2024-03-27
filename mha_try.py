from sw_decima import Bert_decision
import hw_config as cfg
import numpy as np
import pickle as pk
from evaluator import evaluate
import sw_decima as sd

bus_width = 256
is_depth = 32
al = 64
pc = 32
scr = 32
os_depth = 2048

op_target = 'ee_L2'

acc0 = cfg.hwc(config = cfg.Config(bus_width = bus_width, is_depth = is_depth, al = al, pc = pc, scr = scr, os_depth = os_depth))

# return_metric, decision, total_area = Bert_decision(acc0, seq_len=64, hidden_size=1024, head_num=12, num_layers=12, op_target=op_target)


# print(return_metric)
# print(decision)
# print(total_area)

#gli = ('proj',(128,64,128))
gli = ('a2a', (16, 1024, 16))

#op_2ph = sd.block_decision(acc0, gli , 'EDP')[0]['op']

op_2ph = sd.block_decision(acc0, ('proj', (gli[1][1]/gli[1][2], gli[1][0], gli[1][0])), 'EDP')[0]['op']

print(op_2ph)





