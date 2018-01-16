#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a TCP SYN Scanner using Scapy

from scapy.all import *

victim_ip = "127.0.0.1"
start_port_nbr = 1
end_port_nbr = 65535


def is_port_open(pkt):
    # SYN/ACK set
    return pkt[TCP].flags == 18


def scan():
    for p in range(start_port_nbr, end_port_nbr):
        pkt = IP(dst=victim_ip)/\
                  TCP(dport=p, flags="S")
        # print(pkt.summary())
        ans = sr1(pkt, verbose=False, timeout=.2)
        if ans is not None and is_port_open(ans):
            print('Port #: ', p,' appears open')


print("Starting SYN port scan...")
scan()