
from datetime import datetime
import socket
import time

server_address = ('224.0.0.1',4444)
stringname = "GPRMC"
timecode = 0
receiver_warning = "A"
lat = 0
lat_hem = 0
long = 0
long_hem = 0
sog = 0
course = 0
date = 0
mag = 0
checksum = 0
vardir = 0

def gettime():
    utctime = str(datetime.utcnow())
    splittime = utctime.split()
    utcstring = splittime[1].replace(':', '')
    utcsplit = utcstring.split('.')
    utcstring = utcsplit[0]
    return utcstring

def getdate():
    utcdate = str(datetime.utcnow())
    utcsplit = utcdate.split()
    utcdatesplit = utcsplit[0].split('-')
    year = utcdatesplit[0]
    month = utcdatesplit[1]
    day = utcdatesplit[2]
    shortyear = year[2] + year[3]
    utcstring = day + month + shortyear
    return utcstring

def calculate_checksum(nmea):
    csum = 0
    for x in range(len(nmea)):
        csum = csum ^ ord(nmea[x])
    csum = hex(csum)
    csum = csum[2].upper() + csum[3].upper()
    if len(str(csum)) < 2:
        csum = '00' + csum
    return csum

#lat = str(input("Enter Lat, example (4916.45): "))
#lat_hem = str(input("N/S: "))
#long = str(input("Enter Long, example (4916.45): "))
#long_hem = str(input("E/W: "))
#mag = str(input("Enter Magnetic Variation: "))
#sog = str(input("Enter Speed Over Ground: "))
#course = str(input("Enter Course: "))

lat = str("3649.00")
lat_hem = str("S")
long = str("17450.00")
long_hem = str("E")
mag = str("019.0")
sog = str("000.5")
course = str("180.0")
vardir = str("E")


#date = str("150819")
#timecode = str("010820")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    date = str(getdate())
    timecode = str(gettime())
    output = stringname + ',' + timecode + ',' + receiver_warning + ',' + lat + ',' + lat_hem + ',' + long + ',' + long_hem + ',' + sog + ',' + course + ',' + date + ',' + mag + ',' + vardir
    checksum = calculate_checksum(output)
    nmea_string = str('$' + str(output) + '*' + str(checksum) + '\r\n')
    print (nmea_string)
    time.sleep(0.1)
    sock.sendto(nmea_string.encode(), server_address)