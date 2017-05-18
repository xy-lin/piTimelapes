from picamera import PiCamera
from os import system
from time import sleep
import os
import glob
import datetime
import time
import sys

os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
 

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
datafile = open("temperaturedata" + time.strftime('%a-%H-%M-%S') + ".csv", "w") 

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(1)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        
	datafile.write(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H-%M-%S') + "," + str(temp_c) + "\n")
    return temp_c, temp_f

count = 0;

camera = PiCamera()
camera.resolution = (2592, 1944)

i=0;

while True:
    print datetime.datetime.now().time()
    
	#print(read_temp())

    if count==59 :
        count = 0
        datafile.close()
        datafile = open("temperaturedata" + time.strftime('%a-%H-%M-%S') + ".csv", "a")

    count = count + 1   

    #camera.capture('/mnt/timelapes/image{0:06d}.jpg'.format(i))

    for m in range(1, 60):
        for s in range (1,60):
            sleep(1)
            sys.stdout.write("take picture %d waiting %d : %d \r" %(i, m, s))
            sys.stdout.flush()

    i=i+1   

datafile.close()
