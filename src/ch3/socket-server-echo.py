#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Is this server multi-threaded?
# -- Accepts multiple connections, but it's not multithreaded
# - Code up the multi-threaded version of the SocketServer

import socketserver


class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('Got connection from:', self.client_address)
        while True:
            data = self.request.recv(2048)
            if not data:
                print('Client left')
                break
            print('Client sent:', data)
            self.request.send(data)


class ThreadedEchoHandler(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


socketserver.TCPServer.allow_reuse_address = True
serverAddr = ('0.0.0.0', 8000)
server = ThreadedEchoHandler(serverAddr, EchoHandler)
server.serve_forever()