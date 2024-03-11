import hw_config as cfg
import numpy as np

def get_area(acc0):
    gdacc = cfg.hwc(config= cfg.Config())
    gda = np.loadtxt('./Golden_Case/syn_area_rpt.csv', dtype=str, skiprows=1, delimiter=',').astype(float)

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

    estm_area = np.zeros(8)
    # Area.fd.is = f(IS_size)
    estm_area[0] = gda[0]* (linf_paras[0,0]*acc0.IS_size + linf_paras[0,1])/ (linf_paras[0,0]*gdacc.IS_size + linf_paras[0,1])
    # Area.fd.regs = f(InputSRAMWidth)
    estm_area[1] = gda[1]* (linf_paras[1,0]*acc0.InputSRAMWidth + linf_paras[1,1])/ (linf_paras[1,0]*gdacc.InputSRAMWidth + linf_paras[1,1])
    # Area.cm.cims = f(MACRO_ROW*MACRO_COL)
    estm_area[2] = gda[2]* (linf_paras[2,0]*acc0.MACRO_ROW*acc0.MACRO_COL + linf_paras[2,1])/ (linf_paras[2,0]*gdacc.MACRO_ROW*gdacc.MACRO_COL + linf_paras[2,1])
    # Area.cm.regs = f(CIMsComputeWidth)
    estm_area[3] = gda[3]* (linf_paras[3,0]*acc0.CIMsComputeWidth + linf_paras[3,1])/ (linf_paras[3,0]*gdacc.CIMsComputeWidth + linf_paras[3,1])
    # Area.gd.os = f(OS_size)
    estm_area[4] = gda[4]* (linf_paras[4,0]*acc0.OS_size + linf_paras[4,1])/ (linf_paras[4,0]*gdacc.OS_size + linf_paras[4,1])
    # Area.gd.regs = f(OutputSRAMWidth)
    estm_area[5] = gda[5]* (linf_paras[5,0]*acc0.OutputSRAMWidth + linf_paras[5,1])/ (linf_paras[5,0]*gdacc.OutputSRAMWidth + linf_paras[5,1])
    # Area.top.ctrls = f(BusWidth)
    estm_area[6] = gda[6]* (linf_paras[6,0]*acc0.BusWidth + linf_paras[6,1])/ (linf_paras[6,0]*gdacc.BusWidth + linf_paras[6,1])
    
    estm_area[7] = sum(estm_area[:])                

    return estm_area



