# This program reads and labels EMG training data from an Arduino

#pip install pyserial
import serial
import time
import pandas as pd

RUNTIME = 60

port = 'COM3'
ser = serial.Serial(port, 9600, timeout=1)

print("Getting EMG Bicep Training Data")

time.sleep(2)
data = []

label = 1

program_start_time = time.time()
window_start_time = time.time()
while(time.time() - program_start_time < RUNTIME):
    line = ser.readline()   # read a byte string
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        num = float(string) # convert the unicode string to an int
        print(num)
        cur_time = time.asctime( time.localtime(time.time()) ).split()[3]
        data.append([cur_time, num, label]) # add int to data list
    if time.time() - window_start_time > 2:
        window_start_time = time.time()
        if label == 1:
            label = 0
            print("Stop Flexing (just relax)")
        else:
            label = 1
            print("Flex")
        


ser.close()
df = pd.DataFrame(data)
df.to_csv("bicep_flexion.csv")

#https://pythonforundergradengineers.com/python-arduino-potentiometer.html
