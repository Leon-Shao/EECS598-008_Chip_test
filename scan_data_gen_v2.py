'''
functions for generating ft232h scan chain initial data
'''
import os

# length of scan chain
word_length = 533

# write to csv as what we expect it to be
# name, value, #bit, #th bit, idx
# def write_initial(filepath):
#     if os.path.exists(filepath):
#         os.remove(filepath)
#     with open(filepath, 'a', encoding='utf-8') as f:
#         #####################
#         # set FE DBG 
#         #####################
#         f.write(f"FE_EXT_CLK, 1, 1, 0, 0 \n")
#         f.write(f"FE_EXT_RSTB, 0, 1, 1, 1 \n")
#         f.write(f"FE_EXT_RDY, 0, 1, 2, 2 \n")
#         f.write(f"FE_EXT_EN, 0, 1, 3, 3 \n")
#         f.write(f"FE_EXT_ADC, 0, 2048, 4, 4 \n")
#         f.write(f"FE_DBG_SAL_EN, 0, 1, 2052, 5 \n")
#         f.write(f"FE_DBG_SAL_MODE, 0, 2, 2053, 6 \n")
#         f.write(f"FE_FFT_SCAN_RD_ADDR, 0, 7, 2055, 7 \n")
#         f.write(f"FE_MEL_SCAN_RD_ADDR, 0, 5, 2062, 8 \n")
#         f.write(f"FE_LOG_SCAN_RD_ADDR, 0, 5, 2067, 9 \n")
#         #####################
#         # set FE SRAM DBG 
#         #####################
#         f.write(f"FE_DBG_SRAM_EN, 0, 1, 2072, 10 \n")
#         f.write(f"FE_DBG_SRAM_WEN, 1, 1, 2073, 11 \n")
#         f.write(f"FE_DBG_SRAM_CEN, 1, 1, 2074, 12 \n")
#         f.write(f"FE_DBG_SRAM_SEL, 0, 2, 2075, 13 \n")
#         f.write(f"FE_DBG_SRAM_ADDR, 0, 5, 2077, 14 \n")
#         f.write(f"FE_DBG_SRAM_WRITE_DATA, 0, 48, 2082, 15 \n")
#         f.write(f"FE_DBG_SRAM_RTSEL, 170, 8, 2130, 16 \n")
#         f.write(f"FE_DBG_SRAM_WTSEL, 0, 8, 2138, 17 \n")
#         #####################
#         # set CTRL
#         #####################
#         f.write(f"RESETB, 0, 1, 2146, 18 \n")
#         f.write(f"START_KWS, 0, 1, 2147, 19 \n")
#         f.write(f"CNT_AFE_PU_TARGET, 0, 7, 2148, 20 \n")
#         f.write(f"CNT_FE_PU_TARGET, 0, 7, 2155, 21 \n")
#         f.write(f"CNT_NN_PU_TARGET, 0, 7, 2162, 22 \n")
#         f.write(f"START_H_RESET_CNT, 0, 1, 2169, 23 \n")
#         f.write(f"NSKIP_CLIP_EN, 0, 1, 2170, 24 \n")
#         f.write(f"MAX_NSKIP, 0, 6, 2171, 25 \n")
#         f.write(f"RESET_CNT_TARGET, 0, 10, 2177, 26 \n")
#         f.write(f"RESET_COND_OPTION, 0, 2, 2187, 27 \n")
#         f.write(f"PG_ON_AFE_BLK, 0, 1, 2189, 28 \n")
#         f.write(f"PG_ON_FE_BLK, 0, 1, 2190, 29 \n")
#         f.write(f"PG_ON_NN_BLK, 0, 1, 2191, 30 \n")
#         f.write(f"TEST_SINGLE_FRAME, 0, 1, 2192, 31 \n")
#         #####################
#         # set ADC
#         #####################
#         f.write(f"TFAST_SETTLE, 0, 5, 2193, 32 \n")
#         f.write(f"TAMP_STABILIZE, 0, 5, 2198, 33 \n")
#         f.write(f"TSC_FAST, 0, 5, 2203, 34 \n")
#         f.write(f"TSC_NORMAL, 0, 5, 2208, 35 \n")
#         f.write(f"ADC_OFFSET, 0, 8, 2213, 36 \n")
#         f.write(f"ADC_SCALE, 0, 12, 2221, 37 \n")
#         #####################
#         # set NN
#         #####################
#         f.write(f"NN_OFFSET, 0, 8, 2233, 38 \n")
#         f.write(f"NN_SCALE, 0, 12, 2241, 39 \n")
#         f.write(f"WMEM_SCAN_EN, 0, 1, 2253, 40 \n")
#         f.write(f"D_FROM_SCAN, 0,  512, 2254, 41 \n")
#         f.write(f"ADDR_FROM_SCAN, 0, 9, 2766, 42 \n")
#         f.write(f"CEB_FROM_SCAN, 0, 1, 2775, 43 \n")
#         f.write(f"WEB_FROM_SCAN, 0, 1, 2776, 44 \n")
#         f.write(f"CLK_FROM_SCAN, 0, 1, 2777, 45 \n")
#         f.write(f"ED, 1, 3, 2778, 46 \n")
#         f.write(f"SELECT_NN, 0, 1, 2781, 47 \n")
#         f.write(f"CF, 0, 2, 2782, 48 \n")
#         f.write(f"CI, 0, 4, 2784, 49 \n")
#         f.write(f"CL, 0, 3, 2788, 50 \n")
#         f.write(f"I_CTRL0, 0, 3, 2791, 51 \n")
#         f.write(f"I_CTRL1, 0, 3, 2794, 52 \n")
#         f.write(f"I_CTRL2, 0, 3, 2797, 53 \n")
#         f.write(f"I_CTRL0_T, 0, 3, 2800, 54 \n")
#         f.write(f"I_CTRL1_T, 0, 3, 2803, 55 \n")
#         f.write(f"I_CTRL2_T, 0, 3, 2806, 56 \n")
#         f.write(f"PG_ON_T , 0, 1, 2809, 57 \n")
#         f.write(f"RESETB_T, 0, 1, 2810, 58 \n")    
#         #####################
#         # set ETC
#         #####################
#         f.write(f"SIG_VSS, 0, 1, 2811, 59 \n")
#         f.write(f"WR_SCAN_SPARE, 0, 100, 2812, 60 \n")
#         #####################
#         # read signals
#         #####################
#         '''
#         FE_FFT_SCAN #48
#         FE_MEL_SCAN #48
#         FE_LOG_SCAN #8
#         FE_SRAM_DATA #48
#         Q_TO_SCAN #512
#         RD_SCAN_SPARE #100 
#         '''
#         #####################
#         # set RESET
#         #####################
#         #RESET #1

#     return

def read_bin_file_to_val(filepath):
    val_str=''
    with open(filepath,'r') as f:
        lines=f.readlines()
        count=0
        numbit=0
        for line in lines:
            for i in range(len(line)-1):
                numbit+=1
            val_str+=line[0:-1]
            count +=1

    val=int(val_str,2)
    print ("finished reading text file of line length:", count, ", bit: ", numbit)
    return val, numbit

# example for initial data generation from reading binary file input
# name, value, #bit, #th bit, idx
# def write_ext_fe(filepath, adc_data):
#     (val, numbit)=read_bin_file_to_val(adc_data)
#     if numbit!=2048:
#         print("check file!")
#         return 
#     if os.path.exists(filepath):
#         os.remove(filepath)
#     with open(filepath, 'a', encoding='utf-8') as f:
#         #####################
#         # set FE DBG 
#         #####################
#         f.write(f"FE_EXT_CLK, 1, 1, 0, 0 \n")
#         f.write(f"FE_EXT_RSTB, 0, 1, 1, 1 \n")
#         f.write(f"FE_EXT_RDY, 0, 1, 2, 2 \n")
#         f.write(f"FE_EXT_EN, 1, 1, 3, 3 \n")
#         f.write(f"FE_EXT_ADC, {val}, 2048, 4, 4 \n")
#         f.write(f"FE_DBG_SAL_EN, 1, 1, 2052, 5 \n")
#         f.write(f"FE_DBG_SAL_MODE, 0, 2, 2053, 6 \n")
#         f.write(f"FE_FFT_SCAN_RD_ADDR, 0, 7, 2055, 7 \n")
#         f.write(f"FE_MEL_SCAN_RD_ADDR, 0, 5, 2062, 8 \n")
#         f.write(f"FE_LOG_SCAN_RD_ADDR, 0, 5, 2067, 9 \n")
#         #####################
#         # set FE SRAM DBG 
#         #####################
#         f.write(f"FE_DBG_SRAM_EN, 0, 1, 2072, 10 \n")
#         f.write(f"FE_DBG_SRAM_WEN, 1, 1, 2073, 11 \n")
#         f.write(f"FE_DBG_SRAM_CEN, 1, 1, 2074, 12 \n")
#         f.write(f"FE_DBG_SRAM_SEL, 0, 2, 2075, 13 \n")
#         f.write(f"FE_DBG_SRAM_ADDR, 0, 5, 2077, 14 \n")
#         f.write(f"FE_DBG_SRAM_WRITE_DATA, 0, 48, 2082, 15 \n")
#         f.write(f"FE_DBG_SRAM_RTSEL, 170, 8, 2130, 16 \n")
#         f.write(f"FE_DBG_SRAM_WTSEL, 0, 8, 2138, 17 \n")
#         #####################
#         # set CTRL
#         #####################
#         f.write(f"RESETB, 1, 1, 2146, 18 \n")
#         f.write(f"START_KWS, 0, 1, 2147, 19 \n")
#         f.write(f"CNT_AFE_PU_TARGET, 0, 7, 2148, 20 \n")
#         f.write(f"CNT_FE_PU_TARGET, 0, 7, 2155, 21 \n")
#         f.write(f"CNT_NN_PU_TARGET, 0, 7, 2162, 22 \n")
#         f.write(f"START_H_RESET_CNT, 0, 1, 2169, 23 \n")
#         f.write(f"NSKIP_CLIP_EN, 0, 1, 2170, 24 \n")
#         f.write(f"MAX_NSKIP, 0, 6, 2171, 25 \n")
#         f.write(f"RESET_CNT_TARGET, 0, 10, 2177, 26 \n")
#         f.write(f"RESET_COND_OPTION, 0, 2, 2187, 27 \n")
#         f.write(f"PG_ON_AFE_BLK, 0, 1, 2189, 28 \n")
#         f.write(f"PG_ON_FE_BLK, 0, 1, 2190, 29 \n")
#         f.write(f"PG_ON_NN_BLK, 0, 1, 2191, 30 \n")
#         f.write(f"TEST_SINGLE_FRAME, 0, 1, 2192, 31 \n")
#         #####################
#         # set ADC
#         #####################
#         f.write(f"TFAST_SETTLE, 0, 5, 2193, 32 \n")
#         f.write(f"TAMP_STABILIZE, 0, 5, 2198, 33 \n")
#         f.write(f"TSC_FAST, 0, 5, 2203, 34 \n")
#         f.write(f"TSC_NORMAL, 0, 5, 2208, 35 \n")
#         f.write(f"ADC_OFFSET, 0, 8, 2213, 36 \n")
#         f.write(f"ADC_SCALE, 0, 12, 2221, 37 \n")
#         #####################
#         # set NN
#         #####################
#         f.write(f"NN_OFFSET, 0, 8, 2233, 38 \n")
#         f.write(f"NN_SCALE, 0, 12, 2241, 39 \n")
#         f.write(f"WMEM_SCAN_EN, 0, 1, 2253, 40 \n")
#         f.write(f"D_FROM_SCAN, 0,  512, 2254, 41 \n")
#         f.write(f"ADDR_FROM_SCAN, 0, 9, 2766, 42 \n")
#         f.write(f"CEB_FROM_SCAN, 0, 1, 2775, 43 \n")
#         f.write(f"WEB_FROM_SCAN, 0, 1, 2776, 44 \n")
#         f.write(f"CLK_FROM_SCAN, 0, 1, 2777, 45 \n")
#         f.write(f"ED, 0, 3, 2778, 46 \n")
#         f.write(f"SELECT_NN, 0, 1, 2781, 47 \n")
#         f.write(f"CF, 0, 2, 2782, 48 \n")
#         f.write(f"CI, 0, 4, 2784, 49 \n")
#         f.write(f"CL, 0, 3, 2788, 50 \n")
#         f.write(f"I_CTRL0, 0, 3, 2791, 51\n")
#         f.write(f"I_CTRL1, 0, 3, 2794, 52 \n")
#         f.write(f"I_CTRL2, 0, 3, 2797, 53 \n")
#         f.write(f"I_CTRL0_T, 0, 3, 2800, 54 \n")
#         f.write(f"I_CTRL1_T, 0, 3, 2803, 55 \n")
#         f.write(f"I_CTRL2_T, 0, 3, 2806, 56 \n")
#         f.write(f"PG_ON_T , 0, 1, 2809, 57 \n")
#         f.write(f"RESETB_T, 0, 1, 2810, 58 \n")    
#         #####################
#         # set ETC
#         #####################
#         f.write(f"SIG_VSS, 0, 1, 2811, 59 \n")
#         f.write(f"WR_SCAN_SPARE, 0, 100, 2812, 60 \n")
#         #####################
#         # read signals
#         #####################
#         '''
#         FE_FFT_SCAN #48
#         FE_MEL_SCAN #48
#         FE_LOG_SCAN #8
#         FE_SRAM_DATA #48
#         Q_TO_SCAN #512
#         RD_SCAN_SPARE #100 
#         '''
#         #####################
#         # set RESET
#         #####################
#         #RESET #1

#     return

######scripts for generating csv########
def write_csv(filepath, static_wen, static_ren, static_addr, static_wdata, static_rdata, static_ready):
    if os.path.exists(filepath):
        os.remove(filepath)
    with open(filepath, 'a', encoding='utf-8') as f:
        #####################
        # set FE DBG 
        #####################
        f.write(f"static_wen, " + static_wen + ", 1, 0, 0 \n")
        f.write(f"static_ren, " + static_ren + ", 1, 0, 0 \n")
        f.write(f"static_addr, " + static_addr + ", 18, 0, 0 \n")
        f.write(f"static_wdata, " + static_wdata + ", 256, 0, 0 \n")
        f.write(f"static_rdata, " + static_rdata + ", 256, 0, 0 \n")
        f.write(f"static_ready, " + static_ready + ", 1, 0, 0 \n")
    return
######scripts for generating csv########

def bin2dec(binlist):
	dec = 0
	for exp, i in enumerate(binlist[::-1]):
		dec = dec + i*2**exp
	return dec 

def dec2bin(num, num_bit):
        return bin(num).replace("0b","").zfill(num_bit)

def read_csv_data(filename):
    datalist=[]
    val_num=0
    bit_num = 0
    with open(filename,'r') as f:
        lines=f.readlines()
        for line in lines:
            tline = line.strip().split(', ')[1:3]
            datalist.append(dec2bin(int(tline[0]),int(tline[1]))[::-1])
            val_num +=1
            bit_num +=int(tline[1])

    print(f"total value = {val_num}")
    print(f"total bitlength = {bit_num}")

    return datalist

# make multiple changes in data list
# write values in bit reverse way
# get input as list : changes=[[idx,val,numbit],[idx,val,numbit], ...]
def change_data_list(datalist, changes):
    modlist = datalist
    for i, change in enumerate(changes):
        modlist[change[0]]=dec2bin(change[1], change[2])[::-1]
        
    #print(f"total modified value = {i+1}")

    return modlist


# make multiple changes in data string
# write values in bit reverse way
# get input as list : changes=[[idx,val,numbit],[idx,val,numbit], ...]
def change_data_string(datastr, changes):
    modstr = datastr
    for i, change in enumerate(changes):
        modstr = modstr[0:change[0]] + dec2bin(change[1], change[2])[::-1] + modstr[change[0]+change[2]:]

    #print(f"total modified value = {i+1}")

    return modstr


def load_scan_data(datalist):
    datastr=''
    for i in range(len(datalist)):
        datastr += datalist[i]
    # fill zeros for the read ports & reset 
    form ='{:<0'+str(word_length)+'}' #leftshift append 0
    datastr_pad=form.format(datastr)

    return datastr_pad

def write_result_file(filepath, out_str):
    # attach
    #if os.path.exists(filepath):
    #    os.remove(filepath)
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(f"static_wen, {out_str[0:0]} \n")
        f.write(f"static_ren, {out_str[1:1]} \n")
        f.write(f"static_addr, {out_str[19:2]} \n")
        f.write(f"static_wdata, {out_str[275:20]} \n")
        f.write(f"static_rdata, {out_str[531:276]} \n")
        f.write(f"static_ready, {out_str[532:532]} \n")
    return 

# def write_result_file_fe(filepath, out_str):
#     # attach
#     with open(filepath, 'a', encoding='utf-8') as f:
#         f.write(f"FE_FFT_SCAN, {int(out_str[2912:2912+48][::-1],2)}, 48, 2912 \n")
#         f.write(f"FE_MEL_SCAN, {int(out_str[2960:2960+48][::-1],2)}, 48, 2960 \n")
#         f.write(f"FE_LOG_SCAN, {int(out_str[3008:3008+8][::-1],2)}, 8, 3008 \n")

#     return     


# EX 1) initial data gen (make your initial gen function like this reference)
write_csv('scan_initial.csv','1','0','81925','8192500000000000000000000000000000000000000000000','819250000000000000000000000000000000000000000000000000','1')
#to generate read address
#write_csv('scan_read.csv','0','1','todo','0','0','0')

# EX 2) Make initial csv file, list, string and modify selected data
'''
write_initial('scan_initial.csv')
init=read_csv_data('scan_initial.csv')
init_str=load_scan_data(init)
#print(init[44:48])
#print(init_str[2775:2781])
#change_one=change_data_list(init, [[43,1,1]])
#print(change_one[43])
#change_one=change_data_string(init_str, [[2775,1,1]])
#print(change_one[2775])
#change_mult=change_data_list(init, [[43,1,1],[44,1,1],[45,1,1],[46,3,3]])
#print(change_mult[43:47])
#change_mult=change_data_string(init_str, [[2775,1,1],[2776,1,1],[2777,1,1],[2778,4,3]])
#print(change_mult[2775:2781])
'''
