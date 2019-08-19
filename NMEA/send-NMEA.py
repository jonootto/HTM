import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('224.0.0.1',4444)

# src = input("Source File Name: ")
while 1:
    with open('./pos.txt','r') as f:
        for line in f:
            print(line)
            sock.sendto(line.encode(), server_address)
            time.sleep(0.2)