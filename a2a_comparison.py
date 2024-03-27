from evaluator import evaluate
import hw_config as cfg
import numpy as np
import matplotlib.pyplot as plt
import sw_decima as sd
import math as m

def lhd_max_length(acc0, ex_gli):
    max_length = 4
    tst_gli = (ex_gli[0],(max_length, ex_gli[1][1], ex_gli[1][2]))
    while evaluate(acc0, tst_gli, 'lhd') != {}:
        # print("lhd on", max_length, evaluate(acc0, tst_gli, 'lhd')['ee_L2'])
        max_length = max_length*2
        tst_gli = (ex_gli[0],(max_length, ex_gli[1][1], ex_gli[1][2]))
    return max_length

op_target = ['ee_L2', 'EDP', 'throughput']

acc0 = cfg.hwc(config = cfg.Config(bus_width = 256, is_depth = 32, al = 128, pc = 32, scr = 32, os_depth = 2048))

cmpme_lhd = np.zeros((5,6))
cmpme_2ph = np.zeros((5,6))
seq_len  = [16, 64, 128, 256, 512]

x = [0,1,2,3,4]
plot_me = 0

for i in range(5):
    gli = ('a2a', (seq_len[i], 1024, 16))

    # print(lhd_max_length(acc0, gli))

    metric_lhd = evaluate(acc0, gli, 'lhd')

    metric_2ph0, swdec0 = sd.block_decision(acc0, ('proj', (gli[1][0], gli[1][1]/gli[1][2], gli[1][0])), op_target[plot_me])
    metric_2ph1, swdec1 = sd.block_decision(acc0, ('proj', (gli[1][1]/gli[1][2], gli[1][0], gli[1][0])), op_target[plot_me])

    cmpme_lhd[i][3] = metric_lhd['energy_L2']
    cmpme_lhd[i][4] = metric_lhd['op']
    cmpme_lhd[i][5] = metric_lhd['delay']

    cmpme_2ph[i][3] = (metric_2ph0['energy_L2'] + metric_2ph1['energy_L2'])*gli[1][2]
    cmpme_2ph[i][4] = (metric_2ph0['op'] + metric_2ph1['op'])*gli[1][2]
    cmpme_2ph[i][5] = (metric_2ph0['delay'] + metric_2ph1['delay'])*gli[1][2]

    cmpme_lhd[i][0] = cmpme_lhd[i][4] / cmpme_lhd[i][3]
    cmpme_lhd[i][1] = cmpme_lhd[i][4] / cmpme_lhd[i][5]
    cmpme_lhd[i][2] = m.log(cmpme_lhd[i][3] * cmpme_lhd[i][5] ,2)

    cmpme_2ph[i][0] = cmpme_2ph[i][4] / cmpme_2ph[i][3]
    cmpme_2ph[i][1] = cmpme_2ph[i][4] / cmpme_2ph[i][5]
    cmpme_2ph[i][2] = m.log(cmpme_2ph[i][3] * cmpme_2ph[i][5] ,2) 

    plt.scatter(x[i], cmpme_lhd[i][plot_me+3], color='#FF0065')
    plt.scatter(x[i], cmpme_2ph[i][plot_me+3], color='lightseagreen')

print(cmpme_lhd[:,3:6])
print(cmpme_2ph[:,3:6])
print(swdec0,swdec1)

plt.plot(x, cmpme_lhd[:,plot_me+3], color='#FF0065', linestyle = '--', label = 'lhd')
plt.plot(x, cmpme_2ph[:,plot_me+3], color='lightseagreen', linestyle = '--', label = '2ph')
plt.ylim(0)

plt.legend()
plt.xticks(x,labels=seq_len)
plt.show()





