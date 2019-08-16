
import datetime
import socket
import time
from validator_collection import validators, checkers, errors

server_address = ('224.0.0.1',4444)

timecode = 0
receiver_warning = "A"
lat = 0
lat_hem = 0
longt = 0
long_hem = 0
sog = 0
course = 0
date = 0
mag = 0
checksum = 0
vardir = 0
output = ''

def gettime():
    import datetime
    utctime = datetime.datetime.utcnow()
    utctime = str(utctime)
    splittime = utctime.split()
    utcstring = splittime[1].replace(':', '')
    utcsplit = utcstring.split('.')
    utcstring = str(utcsplit[0])
    return utcstring

def getdate():
    import datetime
    utcdate = datetime.datetime.utcnow()
    utcdate = str(utcdate)
    utcsplit = utcdate.split()
    utcdatesplit = utcsplit[0].split('-')
    year = utcdatesplit[0]
    month = utcdatesplit[1]
    day = utcdatesplit[2]
    shortyear = year[2] + year[3]
    utcstring = str(day + month + shortyear)
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

def gprmc(latt = '3650.00',lahem = 'S',lon = '17450.00',lohem = 'E',sg = '000.0',cse = '000.0',mvar = '000.0',mvard = 'E'):
    
    tc = str(getdate())
    dte = str(gettime())
    out = 'GPRMC,' + str(tc) + ',A,' + str(latt) + ',' + str(lahem) + ',' + str(lon) + ',' + str(lohem) + ',' + str(sg) + ',' + str(cse) + ',' + str(dte) + ',' + str(mvar) + ',' +str(mvard)
    csum = calculate_checksum(out)
    nstring = str('$' + str(out) + '*' + str(csum) + '\r\n')
    return nstring

#lat = str(input("Enter Lat, example (4916.45): "))
#lat_hem = str(input("N/S: "))
#longt = str(input("Enter Long, example (4916.45): "))
#long_hem = str(input("E/W: "))
#mag = str(input("Enter Magnetic Variation: "))
#sog = str(input("Enter Speed Over Ground: "))
#course = str(input("Enter Course: "))

lat = str("3649.00")
lat_hem = str("S")
longt = str("17450.00")
long_hem = str("E")
mag = str("019.0")
sog = str("000.5")
course = str("180.0")
vardir = str("E")

def inputs():
    print('NMEA GPRMC Generator')

    i_lat = ''
    i_lat_hem = ''
    i_longt = ''
    i_long_hem = ''
    i_mag =''
    i_sog = ''
    i_course = ''
    i_vardir = ''


    while i_lat == '':
        try:
            i_lat = validators.decimal(input("Input latitude [DDMM.mm]: "),False,0,18000)
        except:
            print('Invalid Input')
            time.sleep(0.5)

    while i_lat_hem == '':
        try:
            i_lat_hem = validators.string(input("Input Hemisphere [N/S]: "),False,False,1,1)
            i_lat_hem = i_lat_hem.upper()
            if (not i_lat_hem == 'N') and (not i_lat_hem == 'S'):
                i_lat_hem = ''
                time.sleep(0.5)
                print('Invalid Input')
        except:
            print('Invalid Input')
            time.sleep(0.5)


    while i_longt == '':
        try:
            i_longt = validators.decimal(input("Input longitude [DDMM.mm]: "),False,0,18000)
        except:
            print('Invalid Input')
            time.sleep(0.5)

    while i_long_hem == '':
        try:
            i_long_hem = validators.string(input("Input Hemisphere [E/W]: "),False,False,1,1)
            i_long_hem = i_long_hem.upper()
            if (not i_long_hem == 'E') and (not i_long_hem == 'W'):
                i_long_hem = ''
                time.sleep(0.5)
                print('Invalid Input')
        except:
            print('Invalid Input')
            time.sleep(0.5)

    while i_mag == '':
        try:
            i_mag = validators.decimal(input("Input Magnetic Variation [DD.dd]: "),False,0,180)
        except:
            print('Invalid Input')
            time.sleep(0.5)

    while i_vardir == '':
        try:
            i_vardir = validators.string(input("Input Hemisphere [E/W]: "),False,False,1,1)
            i_vardir = i_vardir.upper()
            if (not i_vardir == 'E') and (not i_vardir == 'W'):
                i_vardir = ''
                time.sleep(0.5)
                print('Invalid Input1')
        except:
            print('Invalid Input2')
            time.sleep(0.5)

    while i_sog == '':
        try:
            i_sog = validators.decimal(input("Input Speed Over Ground [kt.kt]: "),False,0,100000)
        except:
            print('Invalid Input')
            time.sleep(0.5)            

    while i_course == '':
        try:
            i_course = validators.decimal(input("Input Course [DD.dd]: "),False,0,360)
        except:
            print('Invalid Input')
            time.sleep(0.5)   



    return i_lat,i_lat_hem,i_longt,i_long_hem,i_mag,i_sog,i_course,i_vardir
        
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
lat,lat_hem,longt,long_hem,sog,course,mag,vardir = inputs()

while True:

    nmea_string = gprmc(lat,lat_hem,longt,long_hem,sog,course,mag,vardir)
    print (nmea_string)
    sock.sendto(nmea_string.encode(), server_address)
    time.sleep(1)