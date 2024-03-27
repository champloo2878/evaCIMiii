import numpy as np
import pickle as pk
import hw_config as cfg

#area: 0: fd_is, 1: fd_reg, 2: cims, 3: macros_reg, 4: gd_os, 5: gd_reg, 6: top_reg, 7:total_area;

def power_modeling(acc0):

    instructions = [
            "Lin", # 0
            "Linp", # 1
            "Lwt", # 2
            "Lwtp", # 3
            "Cmpfis_aor", # 4
            "Cmpfis_tos", # 5
            "Cmpfis_aos", # 6
            "Cmpfis_ptos", # 7
            "Cmpfis_paos", # 8 
            "Cmpfgt_aor", # 9   
            "Cmpfgt_tos", # 10
            "Cmpfgt_aos", # 11
            "Cmpfgt_ptos", # 12
            "Cmpfgt_paos", # 13
            "Cmpfgtp", # 14
            "Lpenalty", # 15
            "Nop", # 16
            "Nop_w_rd" # 17
            ]

    power = np.zeros((18,8))

    for i in range(18):
        with open("./power_paras/"+instructions[i]+".pk","rb") as pkf:
            kbs = pk.load(pkf)
            # fd.is
            power[i][0] = (acc0.AL/64)*(acc0.InputSRAMDepth*kbs[0][0] + kbs[0][2])
            # fd.reg 
            power[i][1] = acc0.BusWidth*kbs[1][0] + acc0.AL*kbs[1][1] + kbs[1][2]
            # cims
            power[i][2] = (acc0.AL*acc0.PC/64/8) * kbs[2][0] + kbs[2][2]
            # cim_reg
            power[i][3] = acc0.AL*kbs[3][0] + acc0.PC*kbs[3][1] + kbs[3][2]
            # gd_os
            power[i][4] = (acc0.PC/8)*(acc0.OutputSRAMDepth*kbs[4][0] + kbs[4][2])
            # gd_reg
            power[i][5] = acc0.PC*kbs[5][0] + acc0.BusWidth*kbs[5][1] + kbs[5][2]
            # top_reg
            power[i][6] = acc0.BusWidth*kbs[6][0] + kbs[6][2]
            power[i][7] = power[i][0] + power[i][1] + power[i][2] + power[i][3] + power[i][4] + power[i][5] + power[i][6]

    # bad case correct:
    power[4][0] = power[5][0]
    power[4][2] = power[5][2]
    i = 4
    power[i][7] = power[i][0] + power[i][1] + power[i][2] + power[i][3] + power[i][4] + power[i][5] + power[i][6]

    return power



if __name__ == "__main__":
    acc0 = cfg.hwc(config = cfg.Config(bus_width = 128,
                                   is_depth = 256,
                                   al = 512,
                                   pc = 64,
                                   # scr = 16,
                                   os_depth = 512
                                   ))

    print(power_modeling(acc0))
