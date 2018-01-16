#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a sniffer which uses a filter to only print details of an HTTP packet (TCP, Port 80)
# - Also dump the data

import socket
import struct
import binascii


def is_ip_packet(ethernet_type):
    return ethernet_type == '0800'


def is_tcp_upd(protocol_type_arg):
    return is_tcp(protocol_type_arg) or is_udp(protocol_type_arg)


def is_tcp(protocol_type_arg):
    return protocol_type_arg == '06'


def is_udp(protocol_type_arg):
    return protocol_type_arg == '11'


def parse_ip(packet):
    # IP Header
    ipHeader = packet[0][14:34]
    ip_hdr = struct.unpack("!9s1s2s4s4s", ipHeader)
    ip_protocol = binascii.hexlify(ip_hdr[1])
    source_addr = socket.inet_ntoa(ip_hdr[3])
    dest_addr = socket.inet_ntoa(ip_hdr[4])
    print("Source IP address: ", source_addr)
    print("Destination IP address: ", dest_addr)
    print("Protocol type: ", ip_protocol)
    return source_addr, dest_addr, ip_protocol


def parse_tcp_upd(packet):
    tcpHeader = packet[0][34:54]
    tcp_hdr = struct.unpack("!2s2s16s", tcpHeader)
    src_port = int(binascii.hexlify(tcp_hdr[0]), 16)
    dst_port = int(binascii.hexlify(tcp_hdr[1]), 16)
    print("Source port: ", src_port)
    print("Destination port: ", dst_port)
    return src_port, dst_port


def is_http(src_port, dst_port):
    http_port = 80
    return src_port == http_port or dst_port == http_port


def parse_http(packet):
    http_data = packet[0][54:]
    print("Http data: ", http_data)
    return http_data


def parse_ethernet(packet):
    # Ethernet Header
    ethernetHeader = packet[0][0:14]
    eth_hdr = struct.unpack("!6s6s2s", ethernetHeader)
    source_addr = binascii.hexlify(eth_hdr[0])
    dest_addr = binascii.hexlify(eth_hdr[1])
    eth_type = binascii.hexlify(eth_hdr[2])
    print("Ethernet Destination Host: ", source_addr)
    print("Ethernet Source Host: ", dest_addr)
    print("Ethernet Type: ", eth_type)
    return source_addr, dest_addr, eth_type


# 0x0800 Internet Protocol
rawSocket = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

# Dummy solution - Infinite cycle
while True:
    pkt = rawSocket.recvfrom(2048)
    _, _, eth_type = parse_ethernet(pkt)

    if is_ip_packet(eth_type):
        _, _, protocol_type = parse_ip(pkt)
        if is_tcp_upd(protocol_type):
            source_port, dest_port = parse_tcp_upd(pkt)
            if is_http(source_port, dest_port):
                parse_http(pkt)

