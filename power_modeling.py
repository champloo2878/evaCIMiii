import hw_config as cfg
import numpy as np

def get_power(acc0, gdacc, gdp):
    pass
    linf_paras = np.array(
        [
            [1, 0], # fd.is
            [1, 0], # fd.regs
            [1, 0], # cm.cims
            [1, 0], # cm.regs
            [1, 0], # gd.os
            [1, 0], # gd.regs
            [1, 0]  # top.regs
        ]
    )
    estm_power = np.zeros((18, 8))
    for i in range(18):
        # Power.fd.is = f(IS_size)
        estm_power[i,0] = gdp[i,0]* (linf_paras[0,0]*acc0.IS_size + linf_paras[0,1])/ (linf_paras[0,0]*gdacc.IS_size + linf_paras[0,1])
        # Power.fd.regs = f(InputSRAMWidth)
        estm_power[i,1] = gdp[i,1]* (linf_paras[1,0]*acc0.InputSRAMWidth + linf_paras[1,1])/ (linf_paras[1,0]*gdacc.InputSRAMWidth + linf_paras[1,1])
        # Power.cm.cims = f(MACRO_ROW*MACRO_COL)
        estm_power[i,2] = gdp[i,2]* (linf_paras[2,0]*acc0.MACRO_ROW*acc0.MACRO_COL + linf_paras[2,1])/ (linf_paras[2,0]*gdacc.MACRO_ROW*gdacc.MACRO_COL + linf_paras[2,1])
        # Power.cm.regs = f(CIMsComputeWidth)
        estm_power[i,3] = gdp[i,3]* (linf_paras[3,0]*acc0.CIMsComputeWidth + linf_paras[3,1])/ (linf_paras[3,0]*gdacc.CIMsComputeWidth + linf_paras[3,1])
        # Power.gd.os = f(OS_size)
        estm_power[i,4] = gdp[i,4]* (linf_paras[4,0]*acc0.OS_size + linf_paras[4,1])/ (linf_paras[4,0]*gdacc.OS_size + linf_paras[4,1])
        # Power.gd.regs = f(OutputSRAMWidth)
        estm_power[i,5] = gdp[i,5]* (linf_paras[5,0]*acc0.OutputSRAMWidth + linf_paras[5,1])/ (linf_paras[5,0]*gdacc.OutputSRAMWidth + linf_paras[5,1])
        # Power.top.ctrls = f(BusWidth)
        estm_power[i,6] = gdp[i,6]* (linf_paras[6,0]*acc0.BusWidth + linf_paras[6,1])/ (linf_paras[6,0]*gdacc.BusWidth + linf_paras[6,1])
        
        estm_power[i,7] = sum(estm_power[i,:])                

    return estm_power



golden_acc = cfg.hwc(config= cfg.Config())
golden_power = np.loadtxt('./Golden_Case/sorted_power_rpt.csv', dtype=str, skiprows=2, delimiter=',')[:,1:9].astype(float)

acc0 = cfg.hwc(config= cfg.Config(bus_width= 256, is_depth= 1024, al= 128, pc= 16, scr= 16, os_depth= 2048))


acc0_power = get_power(acc0, golden_acc, golden_power)
print(acc0_power)
