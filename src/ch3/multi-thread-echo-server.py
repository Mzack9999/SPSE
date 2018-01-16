#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - create a Multi-Threaded Echo Server

import socket
from threading import Thread


class ClientThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("New server started for ", ip, ":", port)
    
    def run(self):
        while True:
            data = client.recv(2048)
            if not data:
                break
            print('client sent:', data)
            client.send(data)
        client.close()
        return False


tcp_echo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set reuse address after crash
tcp_echo_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_echo_socket.bind(('0.0.0.0', 8000))

tcp_echo_socket.listen(5)
threads = []

while True:
    print('Waiting for a client...')
    (client, (ip, sock)) = tcp_echo_socket.accept()
    # set timeout of 60 seconds
    client.settimeout(60)
    newThread = ClientThread(ip, sock)
    newThread.start()
    threads.append(newThread)
    newThread.join()