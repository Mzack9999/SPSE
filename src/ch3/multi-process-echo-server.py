#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a Multi-Process Echo Server

import socket
import multiprocessing


def handle_client(client, ip):
    print('Received connection from...', ip)
    while True:
        data = client.recv(2048)
        if not data:
            print("socket closed remotely")
            break
        print('client sent:', data)
        client.send(data)
    client.close()


def handle_exit():
    # Shutting down all the processes
    for process in multiprocessing.active_children():
        print("Shutting down process %r", process)
        process.terminate()
        process.join()


tcp_echo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set reuse address after crash
tcp_echo_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcp_echo_socket.bind(('0.0.0.0', 8000))

tcp_echo_socket.listen(1)
threads = []

while True:
    try:
        print('Waiting for a client...')
        (client, (ip, sock)) = tcp_echo_socket.accept()
        print('Received connection from...', ip)
        print('Starting echo output...')
        # set timeout of 60 seconds
        client.settimeout(60)

        process = multiprocessing.Process(target=handle_client, args=(client, ip))
        process.daemon = True
        process.start()
        print("Started process %r", process)
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating processes...")
        handle_exit()
        print('Shutting down server...')
        tcp_echo_socket.close()
        exit()