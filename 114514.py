import pickle as pk
import numpy as np
import matplotlib.pyplot as plt


def cut_for_plot(filename):
    with open(filename,"rb") as f:
        dse_res = pk.load(f)
    
    cut_res = np.zeros((len(dse_res),2))
    for i in range(len(dse_res)):
        cut_res[i][0] = dse_res[i][0]
        cut_res[i][1] = dse_res[i][1]
    
    with open("cut_"+filename,"wb") as f:
        pk.dump(cut_res, f)

cut = 0
op_target = 'EDP'

if cut:
    cut_for_plot("bert_large_N64_dse_EDP.pk")
    cut_for_plot("bert_large_N64_dse_ee_L2.pk")
    cut_for_plot("bert_large_N64_dse_throughput.pk")


with open("cut_bert_large_N64_dse_"+op_target+".pk","rb") as f:
    dse_res = pk.load(f)

plt.scatter(dse_res[:,0],dse_res[:,1])

max_point = np.argmin(dse_res[:,1])

plt.scatter(dse_res[max_point,0],dse_res[max_point,1],marker='*',s=150,color='#FF0065')

with open("bert_large_N64_dse_"+op_target+".pk","rb") as f:
    dse_res = pk.load(f)

print(dse_res[max_point])

plt.show()


