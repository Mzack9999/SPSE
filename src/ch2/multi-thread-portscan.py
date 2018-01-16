#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a multi-threaded port scanner which uses SYN scanning
# - Recommendation: Divide port range in 10 equal parts and assign each one to a thread which uses Scapy

import Queue
from threading import Thread
from scapy.all import *

conf.verb = 3
ip_target = "127.0.0.1"
port_number_start = 1
port_number_end = 65535

print("Global scanning range: %d - %d" % (port_number_start, port_number_end))

num_threads = 10


def syn_scan(q):
    while True:
        port = q.get()
        resp = sr1(IP(dst=ip_target)/TCP(dport=port,flags="S"), verbose=1, timeout=0.2)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 18:  
            print("port {} is open".format(port))
        q.task_done()


print("Creating queue...")
q = Queue.Queue()

for x in range(num_threads):
    print("Daemonizing Thread %d..." % x)
    worker = Thread(target=syn_scan, args=(q, ))
    worker.setDaemon(True)
    worker.start()
    print("Thread %d Daemonized!" % x)

# Add ports to queue
print("Populating queue....")
for port in range(port_number_start, port_number_end):
    q.put(port)

q.join()
