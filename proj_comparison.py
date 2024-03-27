from evaluator import evaluate
import hw_config as cfg
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist


acc0 = cfg.hwc(config = cfg.Config(bus_width = 256, is_depth = 32, al = 128, pc = 8, scr = 8, os_depth = 2048))


gli = ('proj', (64,1024,1024))

dataflow = ['isap','ispp','wsap','wspp','r_isap','r_ispp','r_wsap','r_wspp']
metric_rec = [0 for i in range(8)]


metric_rec[0] = evaluate(acc0, gli, 'isap')
metric_rec[1] = evaluate(acc0, gli, 'ispp')
metric_rec[2] = evaluate(acc0, gli, 'wsap')
metric_rec[3] = evaluate(acc0, gli, 'wspp')

rv_gli = (gli[0],(gli[1][2],gli[1][1],gli[1][0]))

metric_rec[4] = evaluate(acc0, rv_gli, 'isap')
metric_rec[5] = evaluate(acc0, rv_gli, 'ispp')
metric_rec[6] = evaluate(acc0, rv_gli, 'wsap')
metric_rec[7] = evaluate(acc0, rv_gli, 'wspp')

cmpme = np.zeros((8,3))

for i in range(8):
    cmpme[i][0] = metric_rec[i]['ee_L2']
    cmpme[i][1] = metric_rec[i]['throughput']
    cmpme[i][2] = metric_rec[i]['EDP']

host = host_subplot(111, axes_class=axisartist.Axes)
plt.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)

dfx = [i for i in range(8)]
Throughputs = cmpme[:,1]
EE = cmpme[:,0]
EDP = cmpme[:,2]

msize = 150
host.plot(dfx, Throughputs, linestyle='--', color='black')
host.scatter(dfx, Throughputs, marker='P', s=msize, color='black')
par1.plot(dfx, EE, linestyle='--', color='#FF0067')
par1.scatter(dfx, EE, marker='^', s=msize, color='#FF0067')
par2.plot(dfx, EDP, linestyle='--', color='lightseagreen')
par2.scatter(dfx,EDP, marker='s', s=msize, color='lightseagreen')

plt.xticks(dfx, ['isap', 'wsap', 'ispp', 'wspp', 'r-isap', 'r-wsap', 'r-ispp', 'r-wspp'])
host.set_ylim(0,)
par1.set_ylim(0,)
par2.set_ylim(0,)
host.set_ylabel("Throughput (GOPS)")
par1.set_ylabel("EE w/.L2 read (TOPS/W)")
par2.set_ylabel("EDP (nJs)")

host.axis["left"].label.set_color('black')
par1.axis["right"].label.set_color('#FF0067')
par2.axis["right"].label.set_color('lightseagreen')


plt.show()


