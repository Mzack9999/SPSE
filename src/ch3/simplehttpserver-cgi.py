#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Using SimpleHTTPServer
# - Is there a module available to run CGI as well?
# - Implemented a POC

import CGIHTTPServer

server_address = ('0.0.0.0', 8000)

# Dummy handler
handler = CGIHTTPServer.CGIHTTPRequestHandler

# Define CGI Directory
handler.cgi_directory = '/tmp'

# Start a dummy HTTP server with Cgi support
cgi_http_server = CGIHTTPServer.BaseHTTPServer.HTTPServer(server_address, handler)

# Serve forever unless Keyboard Ctrl + C
try:
    cgi_http_server.serve_forever()
except KeyboardInterrupt:
    # Ctrl + c terminate the server
    cgi_http_server.socket.close()