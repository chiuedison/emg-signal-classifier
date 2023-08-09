#pip install pyserial
import serial
import time
import pandas as pd

port = 'COM3'
ser = serial.Serial(port, 9600, timeout=1)


time.sleep(2)
data = []
for i in range(300):
    line = ser.readline()   # read a byte string
    if line:
        string = line.decode()  # convert the byte string to a unicode string
        num = float(string) # convert the unicode string to an int
        print(num)

        cur_time = time.asctime( time.localtime(time.time()) ).split()[3]

        data.append([cur_time, num]) # add int to data list

    time.sleep(.05)
ser.close()
df = pd.DataFrame(data)
df.to_csv("bicep_flexion.csv")

#https://pythonforundergradengineers.com/python-arduino-potentiometer.html
