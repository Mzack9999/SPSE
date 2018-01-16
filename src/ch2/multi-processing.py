#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Explore the multiprocessing module in python
# -- Requires Python >= 2.6
# - How does it leverage multi-core setups
# -- Splitting the data according to atomic operations (cons: needs more coding)
# --- from multiprocessing import Process, Queue
# -- It can leverage the same result with a Pool object and a number of workers (pro: cleaner code) 
# --- from multiprocessing import Pool
# - Program the TCP SYN scanner using multiprocessing

from multiprocessing import Pool
from scapy.all import *

conf.verb = 3
ip_target = "127.0.0.1"
port_number_start = 1
port_number_end = 65535
port_chunk_size = 500

print("Global scanning range: %d - %d" % (port_number_start, port_number_end))

num_workers = 10


def syn_scan(port_chunk):
    port_start, port_end = port_chunk
    for port in range(port_start, port_end):
        print(port)
        resp = sr1(IP(dst=ip_target)/TCP(dport=port,flags="S"), verbose=0, timeout=0.2)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 18:  
            print("port {} is open".format(port))


print("Creating worker pool...")
pool = Pool(processes=num_workers)

port_chunks = []
# Split global range
n_chunks = int(port_number_end / port_chunk_size)
for n in range(1, n_chunks + 1):
    port_chunks.append((port_chunk_size * (n - 1), port_chunk_size * n))
print(port_chunks)

print("Dispatching job chunks on multi-core architecture")
partial_results = pool.map(syn_scan, port_chunks)