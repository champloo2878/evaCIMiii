import re 
import csv

def extract_data(input_files, output_file, op_code):
    keywords = ["top          ","u_fd","u_input_sram","u_gd","u_output_sram","u_int32_int8","u_macros","u_gd_ctrls","u_penalty","u_macros_ctrls"]
    head_keyword = ["Hierarchy", "Power Group"]
    extract_lines = ["#"*35+3*op_code+"#"*35+"\n"]

    for input_file in input_files:
        with open(input_file, 'r') as f:
            lines = f.readlines()

        already_extracted_keywords = set()
        for i, line in enumerate(lines):
            if "ZeroWireload" not in line:
                if head_keyword[0] in line:
                    if head_keyword[0] not in already_extracted_keywords:
                        extract_lines.extend(lines[max(0, i-1):min(len(lines), i+2)])
                        already_extracted_keywords.add(head_keyword[0])
                elif head_keyword[1] in line:
                    if head_keyword[1] not in already_extracted_keywords:
                        extract_lines.extend(lines[max(0, i-1):min(len(lines), i+15)])
                        already_extracted_keywords.add(head_keyword[1])
                elif any(keyword in line for keyword in keywords):
                    keyword = next(keyword for keyword in keywords if keyword in line)
                    if keyword not in already_extracted_keywords:
                        extract_lines.append(line)
                        already_extracted_keywords.add(keyword)
        extract_lines.append("\n")  

    # extract_lines.append("#"*100+"\n")                        
    with open(output_file, 'a') as f:
        f.writelines(extract_lines)


def extract_data2csv(input_file, output_file, op_codes): 
    pattern_input_sram = re.compile(r"u_input_sram")
    pattern_fd = re.compile(r"u_fd")
    pattern_black_box = re.compile(r"black_box")
    pattern_macros = re.compile(r"u_macros")
    pattern_output_sram = re.compile(r"u_output_sram")
    pattern_gd = re.compile(r"u_gd")
    pattern_top = re.compile(r"top")

    with open(input_file, "r") as f:
        lines = f.readlines()

    with open(output_file, "w", newline = '') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        csvwriter.writerow(['250Mhz @(ssg, 0.81v, -40c)'])
        csvwriter.writerow(['Insruction\Power Break(mW)','fd_input_sram','fd_regs','cm_cims','cm_regs','gd_output_sram','gd_regs','top_ctrl_regs','Total'])
       
        for op_code in op_codes:
            pattern_op_code = re.compile(op_code)
            op_code_index = -1
            for i, line in enumerate(lines):
                if pattern_op_code.search(line):
                    op_code_index = i
                    break

            if op_code_index != -1:
                data_lines = lines[op_code_index+1:op_code_index+29]

                input_sram_value = None
                fd_value = None
                black_box_value = None
                macros_value = None
                output_sram_value = None
                gd_value = None
                top_value = None

                for line in data_lines:
                    if pattern_input_sram.search(line):
                        input_sram_value = str(float(line.split()[-2])*1000)
                    elif pattern_fd.search(line):
                        fd_value = str(float(line.split()[-2])*1000)
                    elif pattern_black_box.search(line):
                        black_box_value = str(float(line.split()[4])*1000)
                    elif pattern_macros.search(line):
                        macros_value = str(float(line.split()[-2])*1000)
                    elif pattern_output_sram.search(line):
                        output_sram_value = str(float(line.split()[-2])*1000)
                    elif pattern_gd.search(line):
                        gd_value = str(float(line.split()[-2])*1000)
                    elif pattern_top.search(line):
                        top_value = str(float(line.split()[-2])*1000)
                
                csvwriter.writerow([op_code,input_sram_value, str(float(fd_value)-float(input_sram_value)), black_box_value, str(float(macros_value)-float(black_box_value)), output_sram_value, str(float(gd_value)-float(output_sram_value)), str(float(top_value)-float(fd_value)-float(gd_value)-float(macros_value)), top_value])




if __name__ == "__main__":
    output_file = "./rpt/all_ins_rpt/0308_1338/verbose_sorted.rpt"
    try:
        with open(output_file, 'rb+') as f:
            f.truncate(0)
    except:
        pass
    Lin_rpt = ["./rpt/all_ins_rpt/0308_1338/Lin/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Lin/top_total.rpt"] 
    extract_data(Lin_rpt, output_file, "Lin ")
    Linp_rpt = ["./rpt/all_ins_rpt/0308_1338/Linp/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Linp/top_total.rpt"] 
    extract_data(Linp_rpt, output_file, "Linp ")
    Lwt_rpt = ["./rpt/all_ins_rpt/0308_1338/Lwt/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Lwt/top_total.rpt"] 
    extract_data(Lwt_rpt, output_file, "Lwt ")
    Lwtp_rpt = ["./rpt/all_ins_rpt/0308_1338/Lwtp/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Lwtp/top_total.rpt"] 
    extract_data(Lwtp_rpt, output_file, "Lwtp ")
    Cmpfis_aor_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfis_aor/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfis_aor/top_total.rpt"] 
    extract_data(Cmpfis_aor_rpt, output_file, "Cmpfis_aor ")
    Cmpfis_tos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfis_tos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfis_tos/top_total.rpt"] 
    extract_data(Cmpfis_tos_rpt, output_file, "Cmpfis_tos ")
    Cmpfis_aos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfis_aos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfis_aos/top_total.rpt"] 
    extract_data(Cmpfis_aos_rpt, output_file, "Cmpfis_aos ")
    Cmpfis_ptos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfis_ptos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfis_ptos/top_total.rpt"] 
    extract_data(Cmpfis_ptos_rpt, output_file, "Cmpfis_ptos ")
    Cmpfis_paos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfis_paos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfis_paos/top_total.rpt"] 
    extract_data(Cmpfis_paos_rpt, output_file, "Cmpfis_paos ")
    Cmpfgt_aor_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgt_aor/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgt_aor/top_total.rpt"] 
    extract_data(Cmpfgt_aor_rpt, output_file, "Cmpfgt_aor ")
    Cmpfgt_tos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgt_tos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgt_tos/top_total.rpt"] 
    extract_data(Cmpfgt_tos_rpt, output_file, "Cmpfgt_tos ")
    Cmpfgt_aos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgt_aos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgt_aos/top_total.rpt"] 
    extract_data(Cmpfgt_aos_rpt, output_file, "Cmpfgt_aos ")
    Cmpfgt_ptos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgt_ptos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgt_ptos/top_total.rpt"] 
    extract_data(Cmpfgt_ptos_rpt, output_file, "Cmpfgt_ptos ")
    Cmpfgt_paos_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgt_paos/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgt_paos/top_total.rpt"] 
    extract_data(Cmpfgt_paos_rpt, output_file, "Cmpfgt_paos ")
    Cmpfgtp_rpt = ["./rpt/all_ins_rpt/0308_1338/Cmpfgtp/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Cmpfgtp/top_total.rpt"] 
    extract_data(Cmpfgtp_rpt, output_file, "Cmpfgtp ")
    Lpenalty_rpt = ["./rpt/all_ins_rpt/0308_1338/Lpenalty/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Lpenalty/top_total.rpt"] 
    extract_data(Lpenalty_rpt, output_file, "Lpenalty ")
    Nop_rpt = ["./rpt/all_ins_rpt/0308_1338/Nop/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Nop/top_total.rpt"] 
    extract_data(Nop_rpt, output_file, "Nop ")
    Nop_w_rd_rpt = ["./rpt/all_ins_rpt/0308_1338/Nop_w_rd/top_hie_level5_sort.rpt", "./rpt/all_ins_rpt/0308_1338/Nop_w_rd/top_total.rpt"] 
    extract_data(Nop_w_rd_rpt, output_file, "Nop_w_rd ")
    print("extract verbose sorted report successfully!")
    output_file_csv = "./rpt/all_ins_rpt/0308_1338/sorted_power_rpt.csv"
    try:
        with open(output_file_csv, 'rb+') as f:
            f.truncate(0)
    except:
        pass
    
    op_codes = ['Lin','Linp','Lwt','Lwtp','Cmpfis_aor','Cmpfis_tos','Cmpfis_aos','Cmpfis_ptos','Cmpfis_paos','Cmpfgt_aor','Cmpfgt_tos','Cmpfgt_aos','Cmpfgt_ptos','Cmpfgt_paos','Cmpfgtp','Lpenalty','Nop','Nop_w_rd']
    extract_data2csv(output_file,output_file_csv,op_codes)
    print("extract verbose report to csv successfully!")


