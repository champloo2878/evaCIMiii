from evaluator import evaluate
import hw_config as cfg
import numpy as np

# op_target = ['ee_L2', 'throughput', 'EDP']

def block_decision(acc0, gli, op_target):
    if gli[0]=='proj':
        metric_rec = [0 for i in range(8)]
        dataflow = ['isap','ispp','wsap','wspp','r_isap','r_ispp','r_wsap','r_wspp']
        metric_rec[0] = evaluate(acc0, gli, 'isap')
        metric_rec[1] = evaluate(acc0, gli, 'ispp')
        metric_rec[2] = evaluate(acc0, gli, 'wsap')
        metric_rec[3] = evaluate(acc0, gli, 'wspp')

        rv_gli = (gli[0],(gli[1][2],gli[1][1],gli[1][0]))

        metric_rec[4] = evaluate(acc0, rv_gli, 'isap')
        metric_rec[5] = evaluate(acc0, rv_gli, 'ispp')
        metric_rec[6] = evaluate(acc0, rv_gli, 'wsap')
        metric_rec[7] = evaluate(acc0, rv_gli, 'wspp')

        cmpme = np.zeros(8)
        for i in range(8):
            cmpme[i] = metric_rec[i][op_target]
        print(cmpme)
        if op_target == 'ee_L2' or op_target == 'throughput':
            return metric_rec[np.argmax(cmpme)], dataflow[np.argmax(cmpme)]
        else:
            return metric_rec[np.argmin(cmpme)], dataflow[np.argmin(cmpme)]

    elif gli[0] == 'a2a':
        return evaluate(acc0, gli, 'lhd'), 'lhd'
        

def Bert_decision(acc0, seq_len, hidden_size, head_num, op_target):
    
    m0 = block_decision(acc0, ('proj',(seq_len, hidden_size, hidden_size)), op_target)

    lhd_fg = evaluate(acc0, ('a2a', (seq_len, hidden_size, head_num)), 'lhd') == {}  
    if lhd_fg:
        m10 = block_decision(acc0, ('proj',(seq_len, hidden_size/head_num, seq_len)), op_target)
        m11 = block_decision(acc0, ('proj',(hidden_size/head_num, seq_len, seq_len)), op_target)
    else:
        m1 = block_decision(acc0, ('a2a',(seq_len, hidden_size, head_num)), op_target)
    
    # m2 = m0 # concat, m0 * 4
    
    m3 = block_decision(acc0, ('proj',(seq_len, hidden_size, hidden_size*4)), op_target)
    m4 = block_decision(acc0, ('proj',(seq_len, hidden_size*4, hidden_size)), op_target)

    if lhd_fg:
        decision = [m0[1],m10[1],m11[1],m0[1],m3[1],m4[1]]
    else:
        decision = [m0[1],m1[1],m0[1],m3[1],m4[1]]
    
    print(decision)

    pass


gli = ('proj',(512,1024,1024))
acc0 = cfg.hwc(config = cfg.Config(bus_width = 256, is_depth = 1024, al = 128, pc = 16, scr = 16, os_depth = 2048))

meme = block_decision(acc0, gli, 'ee_L2')
for content in meme[0]:
    print(content,":",meme[0][content])
print(meme[1])

Bert_decision(acc0, seq_len=64, hidden_size=1024, head_num=12, op_target='ee_L2')







