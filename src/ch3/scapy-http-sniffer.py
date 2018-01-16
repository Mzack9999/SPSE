#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a Packet sniffer with Scapy for HTTP protocol and print out
# -- The HTTP Headers
# -- Data in GET/POST

from scapy.all import *
import re


def parse_packet(pkt):
    pkt_raw_layer = pkt.getlayer(Raw)
    if pkt_raw_layer is None:
        pass
    
    pkt_header = str(pkt_raw_layer).split('\r\n')
    for p in pkt_header:
        if re.search("GET", p) or re.search("POST", p) or re.search("HTTP", p):
            print(p, "\n", '---------------------------------------------------')


sniff(iface='eth0', filter="tcp port 80", prn=parse_packet)
print("Shutting down...")