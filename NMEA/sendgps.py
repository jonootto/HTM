# send position form serial to network


import socket
import serial

# ser = serial.Serial(
#     port='COM3',\
#     baudrate=9600,\
#     parity=serial.PARITY_NONE,\
#     stopbits=serial.STOPBITS_ONE,\
#     bytesize=serial.EIGHTBITS,\
#         timeout=0)

ser = serial.Serial('/dev/ttyACM0')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('224.0.0.1',4444)


while True:
     cc=str(ser.readline())
     if (len(cc) != 3):
        output = cc[2:][:-5]
        print(output)
        sock.sendto(output.encode(), server_address)
