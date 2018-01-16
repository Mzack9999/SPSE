#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a Non-Blocking Multiplexed Echo Server using Select()

import select
import socket
from queue import Queue, Empty

# The echo server example from the socket section can be extended to watch for more than one 
# connection at a time by using select(). The new version starts out by creating a non-blocking 
# TCP/IP socket and configuring it to listen on an address.

tcp_echo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_echo_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_echo_socket.setblocking(0)
tcp_echo_socket.bind(('0.0.0.0', 8000))
tcp_echo_socket.listen(5)

# The arguments to select() are three lists containing communication channels to monitor. 
# The first is a list of the objects to be checked for incoming data to be read, 
# the second contains objects that will receive outgoing data when there is room in their buffer, 
# and the third those that may have an error (usually a combination of the input and output channel objects). 
# The next step in the server is to set up the lists containing input sources and output destinations 
# to be passed to select().

# Sockets from which we expect to read
inputs = [ tcp_echo_socket ]

# Sockets to which we expect to write
outputs = [ ]

# Connections are added to and removed from these lists by the server main loop. Since this version of the server 
# is going to wait for a socket to become writable before sending any data (instead of immediately 
# sending the reply), each output connection needs a queue to act as a buffer for the data to be 
# sent through it.

# Outgoing message queues (socket:Queue)
message_queues = {}

# The main portion of the server program loops, calling select() to block and wait for network activity.

while inputs:

    # Wait for at least one of the sockets to be ready for processing
    print('waiting for the next event')
    readable, writable, exceptional = select.select(inputs, outputs, inputs)

    # select() returns three new lists, containing subsets of the contents of the lists passed in. All of the sockets in the readable list have incoming data 
    # buffered and available to be read. All of the sockets in the writable list have free space in their buffer and can be written to. The sockets returned in
    # exceptional have had an error (the actual definition of "exceptional condition" depends on the platform).

    # The "readable" sockets represent three possible cases. If the socket is the main "server" socket, the one being used to listen for connections,
    # then the "readable" condition means it is ready to accept another incoming connection. In addition to adding the new connection to the list of inputs
    # to monitor, this section sets the client socket to not block

    # Handle inputs
    for s in readable:

        if s is tcp_echo_socket:
            # A "readable" server socket is ready to accept a connection
            connection, client_address = s.accept()
            print('new connection from', client_address)
            connection.setblocking(0)
            inputs.append(connection)

            # Give the connection a queue for data we want to send
            message_queues[connection] = Queue()

        # The next case is an established connection with a client that has sent data. The data is read with recv(), then placed on the queue so it 
        # can be sent through the socket and back to the client.
        else:
            data = s.recv(2048)
            if data:
                # A readable client socket has data
                print('received "%s" from %s' % (data, s.getpeername()))
                message_queues[s].put(data)
                # Add output channel for response
                if s not in outputs:
                    outputs.append(s)

            # A readable socket without data available is from a client that has disconnected, and the stream is ready to be closed.
            else:
                # Interpret empty result as closed connection
                print('closing', client_address, 'after reading no data')
                # Stop listening for input on the connection
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remove message queue
                del message_queues[s]

    # There are fewer cases for the writable connections. If there is data in the queue for a connection, the next message is sent. 
    # Otherwise, the connection is removed from the list of output connections so that the next time through the loop select() 
    # does not indicate that the socket is ready to send data.

    # Handle outputs
    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Empty:
            # No messages waiting so stop checking for writability.
            print('output queue for', s.getpeername(), 'is empty')
            outputs.remove(s)
        else:
            print('sending "%s" to %s' % (next_msg, s.getpeername()))
            s.send(next_msg)

    # Finally, if there is an error with a socket, it is closed.

    # Handle "exceptional conditions"
    for s in exceptional:
        print('handling exceptional condition for', s.getpeername())
        # Stop listening for input on the connection
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

        # Remove message queue
        del message_queues[s]