#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a Wi-Fi Sniffer and print out the unique SSIDs of the Wi-Fi networks in your vicinity

from scapy.all import *

bssid_list = []


def parse_packet(pkt):
    if not pkt.haslayer(Dot11Beacon):
        pass
    bssid = pkt[Dot11].addr3
    if bssid not in bssid_list:
        bssid_list.append(bssid)
        print('New bssid: ', bssid)


sniff(iface='mon0', prn=parse_packet)
print("Shutting down...")