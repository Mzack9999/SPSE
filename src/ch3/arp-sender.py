#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Send an ARP Request Packet using Raw Sockets
# - Verify the same with Tcpdump or Wireshark

# PROOF
# root@a5031bbfccac:/# tcpdump
# tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
# listening on eth0, link-type EN10MB (Ethernet), capture size 262144 bytes
# 23:14:18.905663 ARP, Request who-has localhost tell localhost, length 28

import socket
from struct import pack

ARPOP_REQUEST = pack('!H', 0x0001)
# Ethernet protocol type (=ARP)
ETHERNET_PROTOCOL_TYPE_ARP = pack('!H', 0x0806)
# ARP logical protocol type (Ethernet/IP)
ARP_PROTOCOL_TYPE_ETHERNET_IP = pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004)


def send_arp(ip):
    
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.SOCK_RAW)
    s.bind(('eth0', socket.SOCK_RAW))

    socket_mac = sender_mac = s.getsockname()[4]
    
    target_mac = pack('!6B', *(0x00,)*6) # 00:00:00:00:00:00

    sender_ip = pack('!4B', *[int(x) for x in ip.split('.')])
    target_ip = pack('!4B', *[int(x) for x in ip.split('.')])

    arpframe = [
        # ## ETHERNET
        # destination MAC addr
        pack('!6B', *(0xFF,)*6), # FF:FF:FF:FF:FF:FF
        # source MAC addr
        socket_mac,
        ETHERNET_PROTOCOL_TYPE_ARP,
        # ## ARP
        ARP_PROTOCOL_TYPE_ETHERNET_IP,
        # operation type
        ARPOP_REQUEST,
        # sender MAC addr
        sender_mac,
        # sender IP addr
        sender_ip,
        # target hardware addr
        target_mac,
        # target IP addr
        target_ip
    ]

    # send the ARP
    s.send(b''.join(arpframe))
    s.close()


send_arp('127.0.0.1')