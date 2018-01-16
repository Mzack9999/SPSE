#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a DNS Fuzzer with Scapy and try it against DNSspoof

from scapy.all import *

target_ip = '127.0.0.1'

srloop(IP(dst=target_ip)/UDP()/fuzz(DNS()))