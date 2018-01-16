#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a tcp server which listens to a port
# - Implement signals to ensure it automatically shuts down after a pre-configured duration which is given via command line
#   eg tcp-server -s 100
# - Shutdown after listening to port for t (eg. 100) seconds

import signal, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


# Define HTTP Server
class HttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/admin":
            self.wfile.write("This page is only for Admins!")
            self.wfile.write(self.headers)
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


# Signal handler
def signal_handler(signum, frame):
    print("Received SIGALRM signal")
    exit(0)


# Parse command line arguments
parser = argparse.ArgumentParser(description="Temporized HTTP Server")

# Required argument
parser.add_argument('t', type=int, help='Number of seconds to wait before disconnecting')
args = parser.parse_args()

print("Number of seconds: ", args.t)

# Setup Temporized Signal
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(args.t)

# Setup the HTTP Server
httpd = HTTPServer(('localhost', 4443), HttpRequestHandler)
httpd.allow_reuse_address = True
httpd.serve_forever()