
import datetime
import socket
import time
from validator_collection import validators, checkers, errors

server_address = ('224.0.0.1',4444)

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

    i_mag = str("0.0")
    # while i_mag == '':
    #     try:
    #         i_mag = validators.decimal(input("Input Magnetic Variation [DD.dd]: "),False,0,180)
    #     except:
    #         print('Invalid Input')
    #         time.sleep(0.5)
    i_vardir = str("E")
    # while i_vardir == '':
    #     try:
    #         i_vardir = validators.string(input("Input Hemisphere [E/W]: "),False,False,1,1)
    #         i_vardir = i_vardir.upper()
    #         if (not i_vardir == 'E') and (not i_vardir == 'W'):
    #             i_vardir = ''
    #             time.sleep(0.5)
    #             print('Invalid Input1')
    #     except:
    #         print('Invalid Input2')
    #         time.sleep(0.5)

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

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        lat,lat_hem,longt,long_hem,sog,course,mag,vardir = inputs()
        sspeed = -0.00025
        espeed = 0.00010
        while True:
            lat = str(round(float(lat) + sspeed,5))
            longt = str(round(float(longt) + espeed,5))
            nmea_string = gprmc(lat,lat_hem,longt,long_hem,sog,course,mag,vardir)
            print (nmea_string)
            sock.sendto(nmea_string.encode(), server_address)
            time.sleep(0.01)
    except:
        print("error")