
#area: 0: fd_is, 1: fd_reg, 2: cims, 3: macros_reg, 4: gd_os, 5: gd_reg, 6: top_reg, 7:total_area;


# for FD.IS( width = 512 ), Area(depth) = 111.288 * depth + 114700.7
# for FD.REG, Area(AL) = 68.05828 * al + 1619.94

def area_modeling(acc0):
    area = [0 for i in range(8)]
    area[0] = acc0.MACRO_COL * (111.288*acc0.InputSRAMDepth + 114700.7)
    area[1] = acc0.AL * 68.05828 + 1619.94
    area[2] = (acc0.MACRO_COL*acc0.MACRO_ROW) * 206514.5299 - 886.439
    area[3] = acc0.AL*acc0.PC * 1.290714 + 1622.281
    area[4] = acc0.MACRO_ROW * (55.680373377*acc0.OutputSRAMDepth + 115035.87042)
    area[5] = acc0.PC * 1076.61371 + 1581.7796
    area[6] = acc0.BusWidth * 5.50720922 + 1334.05853
    area[7] = area[0] + area[1] + area[2] + area[3] + area[4] + area[5] + area[6] + area[7] 
    return area 







