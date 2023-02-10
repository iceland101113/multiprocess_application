#!/usr/bin/env python
import socket
import struct

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on %s:%d " % (bind_ip,bind_port))

while True:
    client,addr = server.accept()
    print('Connected by ', addr)

    while True:
        data = client.recv(1024).strip().decode()
        raw_a = data.split()
        numbers = []
        for i in raw_a:
            numbers.append(int(i))
        result = sum(numbers)/len(numbers)
        client.send(str(result).encode())