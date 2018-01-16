#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a simple Echo Server to handle 1 client

import socket

tcp_echo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set reuse address after crash
tcp_echo_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_echo_socket.bind(('0.0.0.0', 8000))

tcp_echo_socket.listen(1)

while True:
    print('Waiting for a client...')
    (client, (ip, sock)) = tcp_echo_socket.accept()

    print('Received connection from...', ip)
    print('Starting echo output...')

    while True:
        data = client.recv(2048)
        if not data:
            print('Closing connection...')
            client.close()
            break
        print('client sent:', data)
        client.send(data)

print('Shutting down server...')
tcp_echo_socket.close()