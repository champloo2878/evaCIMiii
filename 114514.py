import pickle as pk
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from mpl_toolkits import axisartist

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

with open("eva_res.pk" ,"rb") as f:
    eva_res = pk.load(f)
'''
for i in range(len(var_name)):
    print("\n")
    print(var_name[i])
    for j in range(8):
        print(eva_res[j][i])


print("\ntotal energy")
for i in range(8):
    print(eva_res[i][0] + eva_res[i][8])

print("\nEE_L1_L2")
for i in range(8):
    print(eva_res[i][3] / (eva_res[i][0] + eva_res[i][8]))
'''

host = host_subplot(111, axes_class=axisartist.Axes)
plt.subplots_adjust(right=0.75)

par1 = host.twinx()
par2 = host.twinx()

par2.axis["right"] = par2.new_fixed_axis(loc="right", offset=(60, 0))
par1.axis["right"].toggle(all=True)
par2.axis["right"].toggle(all=True)

dfx = [i for i in range(8)]
Throughputs = eva_res[:,5]
EE = eva_res[:,3] / (eva_res[:,0] + eva_res[:,8])
print(EE)
EDP = (eva_res[:,0] + eva_res[:,8]) * eva_res[:,4] / 1e12 
print(EDP)

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

