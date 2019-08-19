import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('224.0.0.1',4444)

src = input("Source File Name: ")

f= open(src,"r")

if f.mode == 'r':
    contents = f.read()
