
import datetime
import socket
import time

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

def gprmc(tc ,dte ,latt = '3650.00',lahem = 'S',lon = '17450.00',lohem = 'E',sg = '000.0',cse = '000.0',mvar = '000.0',mvard = 'E'):

    nstring= ''
    out = 'GPRMC,' + str(tc) + ',A,' + str(latt) + ',' + str(lahem) + ',' + str(lon) + ',' + str(lohem) + ',' + str(sg) + ',' + str(cse) + ',' + str(dte) + ',' + str(mvar) + ',' +str(mvard)
    csum = calculate_checksum(out)
    nstring = str('$' + str(out) + '*' + str(csum) + '\r\n')
    return nstring

def dtime():
    global date
    global timestr
    date = str(getdate())
    timestr = str(gettime())

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
    print('Enter Inputs...')
    print(int(1.112))
    
    i_lat = ''
    i_lat_hem = ''
    i_longt = ''
    i_long_hem = ''
    i_mag = inputInt('Enter Magnetic Variation [000]:')
    i_sog = ''
    i_course = ''
    i_vardir = inputChar('Input Magnetic Variation Direction [E]: ')
    return i_lat,i_lat_hem,i_longt,i_long_hem,i_mag,i_sog,i_course,i_vardir


def inputInt(message):
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            userInput = str(userInput)
            return userInput

def inputChar(message):
    while True:
        userInput = input(message)
        userInput = userInput.upper()
        if userInput.isalpha() == True:
            if len(userInput) == 1:
                print(len(userInput))
                return userInput
            else:
                print("Enter one character only")
        else:
            print("Must be a character")
        
        
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while 1:
    lat,lat_hem,longt,long_hem,sog,course,mag,vardir = inputs()
    dtime()
    nmea_string = gprmc(timecode,lat,lat_hem,longt,long_hem,sog,course,date,mag,vardir)
    print (nmea_string)
    time.sleep(0.1)
    sock.sendto(nmea_string.encode(), server_address)
