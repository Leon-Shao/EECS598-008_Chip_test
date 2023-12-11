# SCAN chain test with GPIO Async mode
import time
import numpy as np
from pyftdi import *
from pyftdi.ftdi import Ftdi
from pyftdi.usbtools import UsbTools
#GPIO controller for an FTDI port, in bit-bang asynchronous mode.
from pyftdi.gpio import GpioAsyncController
from functools import lru_cache
import scan_data_gen_v2 as dataload
import os

# integer list, no command width
# Use async controller
# file gen from scan_data_gen_v2.py
# test SCAN behavior with D-Ports
# use pyftdi lib

# list all device if using multiple board need to configure with this url
#vendor id, product id
FT232H_list = UsbTools.find_all([(0x403, 0x6014)])
print(FT232H_list)

# general info
# max sequence length with maximum buffersize(65536) is 10922 bits

# scan info
# scan chain length 3677
#GPIO accessible pins are limited to the 8 lower pins of each GPIO port.
#need  other gpio for clock config/reset control
'''
PIN MAPS
D7 - clk_gate (O)
D6 - scan_id (O)
D5 - scan_data_out (I)
D4 - scan_phi_bar (O)
D3 - scan_phi (O)
D2 - scan_data_in (O) 
D1 - scan_load_chain (O)
D0 - scan_load_chip (O)
---------------

'''
# bit masks for device control
global SCHIP, SCHAIN, SDI, PHI, PHI_B, SCAN_BITS, SCAN_ID, CLK_GATE, PIN_H, PIN_L, init_val

SCHIP = 0x01
SCHAIN = 0x02
SDI = 0x04
PHI = 0x08
PHI_B = 0x10
SCAN_ID = 0x40
CLK_GATE = 0x80

SCAN_BITS = CLK_GATE | SCAN_ID | PHI | PHI_B | SDI | SCHIP | SCHAIN  #0x1F

PIN_L = SCAN_BITS
PIN_H = 0x0000
PIN_A = PIN_H+PIN_L

init_val = 0x0000 & PIN_A
reset_val = init_val

# const for device control
freq =5e6


global packet_length
# global scan_id_reg

scan_id_reg = 0
packet_length = 533
# scan chain length
word_length = 533

@lru_cache(maxsize=2)
def command_write_scanbit(din, vv=0):
    if vv: print ("- command compile, write_do to scan = [%d]"%(din))
    commands = []
    i_din = int(din)
    commands.append(0*SCHAIN+0*SCHIP+i_din*SDI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(15):
        commands.append(0*SCHAIN+0*SCHIP+i_din*SDI+1*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*SCHAIN+0*SCHIP+i_din*SDI+0*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(15):
        commands.append(0*SCHAIN+0*SCHIP+i_din*SDI+1*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*SCHAIN+0*SCHIP+i_din*SDI+0*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)
    
    return commands

def command_read_scanbit(ftdi,peek=True, vv=0): #scan out from chip
    if vv: print("- command compile, read_scanbit")
    commands = []
    commands.append(0*SCHAIN+0*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    ftdi.write(commands)
    if peek:
        data= ftdi.read(1, peek)
        dout = dataload.dec2bin(data,8)[-6]
    else:
        data= ftdi.read(1)
        dout = format(int(data),'#010b')[-6] # D5 is dout

    commands = []
    for i in range(15):
        commands.append(0*SCHAIN+1*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*SCHAIN+0*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(15):
        commands.append(0*SCHAIN+1*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*SCHAIN+0*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)

    ftdi.write(commands)

    return dout

def command_load_chip(vv=0):
    if vv: print("- command compile, load_chip")
    commands = []
    commands.append(0*SCHIP+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(1*SCHIP+1*CLK_GATE+scan_id_reg*SCAN_ID)
    commands.append(0*SCHIP+1*CLK_GATE+scan_id_reg*SCAN_ID)

    return commands

def command_scan_id(scan_id_reg, vv=0):
    if vv: print("- command compile, scan_id")
    # scan_id_reg = not(scan_id_reg)
    commands = []
    commands.append(scan_id_reg*SCAN_ID+1*CLK_GATE)
    #print(scan_id_reg*SCAN_ID)
    return commands

def command_clk_gate(vv=0):
    if vv: print("- command compile, clk_gate")
    commands = []
    commands.append(0*CLK_GATE+scan_id_reg*SCAN_ID)
    commands.append(1*CLK_GATE+scan_id_reg*SCAN_ID)

    return commands

def command_load_chain(vv=0):#scan out from chip
    if vv: print("- command compile, load_chain")
    commands = []
    for i in range(10):
        commands.append(0*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(1*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(15):
        commands.append(1*PHI+1*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*PHI+1*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(15):
        commands.append(1*PHI_B+1*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    for i in range(10):
        commands.append(0*PHI_B+1*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)
    # extra cycle..
    commands.append(0*SCHAIN+1*CLK_GATE+scan_id_reg*SCAN_ID)

    return commands

# peek mode: read instant pin value
def read_scan(ftdi, peek=True, verbose=1, vv=0):
    if verbose: print("scan : reading SCANCHAIN")
    i_iter = int((word_length-1)/packet_length) + int((word_length-1)%packet_length > 0 )
    # load chain
    if verbose: print('scan : loading chain')
    commands = command_load_chain(vv)
    # commands += command_scan_id(scan_id_reg,vv) ###########
    ftdi.write(commands)
    # read chain
    return_str = ''
    temp_datastr = ''
    for i in range(i_iter):
        if i == i_iter-1: 	j_iter = word_length - i*packet_length
        else:			j_iter = packet_length
        for j in range(j_iter):
            temp_datastr += command_read_scanbit(ftdi,peek, vv)
        if verbose: print("scan : reading data =",temp_datastr)
        return_str += temp_datastr
        temp_datastr = ''
    if verbose: print("scan : SUCCESS! read SCANCHAIN")
    return return_str

def read_scan_rotate(ftdi, peek=True, verbose=1, vv=0):
    if verbose: print("scan : reading SCANCHAIN")
    i_iter = int((word_length-1)/packet_length) + int((word_length-1)%packet_length > 0 )

    # read chain
    return_str = ''
    temp_datastr = ''
    for i in range(i_iter):
        if i == i_iter-1: 	j_iter = word_length - i*packet_length
        else:			j_iter = packet_length

        commands = []
        #for i in range(15):
        #    commands.append(0*SCHAIN+1*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
        #for i in range(10):
        #    commands.append(0*SCHAIN+0*PHI+1*CLK_GATE+scan_id_reg*SCAN_ID)
        #for i in range(15):
        #    commands.append(0*SCHAIN+1*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)
        #for i in range(10):
        #    commands.append(0*SCHAIN+0*PHI_B+1*CLK_GATE+scan_id_reg*SCAN_ID)
        
        ftdi.write(commands)
    

        for j in range(j_iter):
            temp_datastr += command_read_scanbit(ftdi,peek, vv)
        if verbose: print("scan : reading data =",temp_datastr)
        return_str += temp_datastr
        temp_datastr = ''
    if verbose: print("scan : SUCCESS! read SCANCHAIN")
    return return_str

def write_scan(ftdi, datastr='', loopback=0, verbose=1, vv=0):
    global scan_id_reg
    if vv: print("scan : writing SCANCHAIN :%s "%(datastr))

    i_datastr = datastr.zfill(word_length)
    #print(i_datastr)
    i_datalist = []
    try:
        for item in i_datastr:
            i_datalist.append(int(item)) #might need bytes
    except ValueError :
        raise DevError('arg "datastr" needs to be a string of integer\n\n')
        return
    i_iter = int((word_length-1)/packet_length) + int((word_length-1)%packet_length > 0 )

    # write chain
    if verbose: print('scan : writing chip')
    temp_datastr = ''
    commands = []
    for i in range(i_iter):
        if i == i_iter-1: 	j_iter = word_length - i*packet_length
        else:			j_iter = packet_length
        for j in range(j_iter):
            commands+=(command_write_scanbit(i_datalist[i*packet_length+j],vv))
            temp_datastr += str(i_datalist[i*packet_length+j])
        if verbose: print("scan : sending data =",temp_datastr)
        temp_datastr = ''
        ftdi.write(commands)

        commands = []
    if verbose: print("scan : sending data =",temp_datastr,' - eom')
    # load chip
    if verbose: print('scan : loading chip')
    commands = command_load_chip(vv)
    scan_id_reg = not(scan_id_reg)
    print(str(scan_id_reg))
    commands+=command_scan_id(scan_id_reg,vv)
    print(len(commands))
    ftdi.write(commands)
    if verbose: print("scan : SUCCESS! wrote SCANCHAIN")
    # loopback test
    if loopback == 1:
        #time.sleep(1)
        if verbose: print("- doing loopback test")
        i_loopbackstr = read_scan(ftdi, verbose,vv)
        if i_datastr == i_loopbackstr: 
            if verbose: print("SUCCESS! sent message correctly")
        else: 
            if verbose: print("FAILED!! loopback message different from sent")
    else:
        if verbose: print("SUCCESS! sent message")
    return 

def rotate(ftdi, datastr='', loopback=1, verbose=1, vv=0):
    global scan_id_reg
    if vv: print("scan : writing SCANCHAIN :%s "%(datastr))

    i_datastr = datastr.zfill(word_length)
    #print(i_datastr)
    i_datalist = []
    try:
        for item in i_datastr:
            i_datalist.append(int(item)) #might need bytes
    except ValueError :
        raise DevError('arg "datastr" needs to be a string of integer\n\n')
        return
    i_iter = int((word_length-1)/packet_length) + int((word_length-1)%packet_length > 0 )

    # write chain
    if verbose: print('scan : writing chip')
    temp_datastr = ''
    commands = []
    for i in range(i_iter):
        if i == i_iter-1: 	j_iter = word_length - i*packet_length
        else:			j_iter = packet_length
        for j in range(j_iter):
            commands+=(command_write_scanbit(i_datalist[i*packet_length+j],vv))
            temp_datastr += str(i_datalist[i*packet_length+j])
        #if verbose: print("scan : sending data =",temp_datastr)
        temp_datastr = ''
        ftdi.write(commands)

    # loopback test
    if loopback == 1:
        #time.sleep(1)
        if verbose: print("- doing loopback test")
        i_loopbackstr = read_scan_rotate(ftdi, verbose,vv)
        print("received data =", i_loopbackstr)
        if i_datastr == i_loopbackstr: 
            if verbose: print("SUCCESS! sent message correctly")
        else: 
            if verbose: print("FAILED!! loopback message different from sent")
            print("idata is", i_datastr)
            print("iloopback is", i_loopbackstr)
            print("error location",bin(int(i_datastr,2)^int(i_loopbackstr,2)))
    else:
        if verbose: print("SUCCESS! sent message")
    return 

class Error(Exception):
    pass

class DevError(Error):
    def __init__(ftdi, expression):
        print(expression)

####################### MAIN ##########################

# GPIO SCAN test v2
# confirm device existence and open handle
mydev = GpioAsyncController()
# configure setting, specify connection details using a URL
mydev.configure("ftdi://ftdi:232h:00:ff/1", direction=PIN_A, frequency=freq, initial=init_val)
mydev._ftdi._usb_write_timeout = 5000
mydev._ftdi._usb_read_timeout = 5000
mydev._ftdi.read_data_set_chunksize(65535)
mydev._ftdi.write_data_set_chunksize(65535)
mydev._ftdi.set_latency_timer(1) 


# Ex1) do reset test
#how to detect async switch toggled?
# mydev._ftdi.purge_buffers()
# time.sleep(1)


# Ex2) do write 
#mydev.write(command_clk_gate()) # Added clock gate

init_list=dataload.read_csv_data('scan_initial1.csv')
for i in range(380):
    init_str=dataload.load_scan_data(init_list[i])
    write_scan(mydev,init_str, 1, 1, 0)
    #rotate(mydev,init_str, 1, 1, 0)  # for rotate chain

#    init_str=dataload.load_scan_data(init_list[i])
#    write_scan(mydev,init_str, 1, 1, 0)


print("scan in finishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

init_list1=dataload.read_csv_data('scan_initial2.csv')
for i in range(4):
   init_str=dataload.load_scan_data(init_list1[i])
   write_scan(mydev,init_str, 0, 0, 0)
   douts=read_scan(mydev,True, 0,0)
   print("dout is", douts)
   dataload.write_result_file('scan_fe_out.csv', douts)
for i in range(1000):
    print("scan in finishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
init_list2=dataload.read_csv_data('scan_initial3.csv')
for i in range(4):
   init_str=dataload.load_scan_data(init_list2[i])
   write_scan(mydev,init_str, 0, 0, 0)
   douts=read_scan(mydev,True, 0,0)
   print("dout is", douts)
   dataload.write_result_file('scan_fe_out1.csv', douts)

print("scan in finishhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
# Ex3) do read (read 3677 data, from 2909th bit chip output)
#init_list=dataload.read_csv_data('scan_read.csv')
#init_str=dataload.load_scan_data(init_list)
#write address you want to read from
#write_scan(mydev,init_str, 1, 1, 0)
#douts=read_scan(mydev,True, 0,0)
#if os.path.exists('scan_out.csv'):
#   os.remove('scan_out.csv')
#dataload.write_result_file('scan_out.csv', douts)

# Ex4) do mfcc scan test

mydev._ftdi.reset()
mydev.close()

