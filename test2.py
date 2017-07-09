import json
import gspread
import os
import glob
import time
from datetime import datetime
from oauth2client.client import SignedJwtAssertionCredentials


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def add_cells():
    print 'connecting ...'
    json_key = json.load(open('bw-key.json'))
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc=gspread.authorize(credentials)
    wks=gc.open("Beer Warmer").sheet1
    d = datetime.today().date()
    dt = d.isoformat()
    t = datetime.now().time()
    tt = t.isoformat()
    print (dt)
    print (tt)
    print (read_temp())
    wks.append_row([dt, tt, read_temp()])  

while True:
    print '----------------------'
    print 'starting add_cells ...'
    add_cells()
    print 'sheet updated ...'
    print '----------------------'
    print ' '
    print ' '
    time.sleep(300)
