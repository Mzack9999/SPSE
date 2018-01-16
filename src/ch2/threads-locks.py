#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - There is a locking mechanism available in the Thread class which you can use to lock resources for dedicated use
# - Create a sample code to illustrate this concept

from threading import Thread, Lock

counter = 0
lock = Lock()
num_threads = 5


def process_item(item):
    global counter
    print("Acquiring thread lock for item %d..." % item)
    with lock:
        print("Processing item %d:" % item)
        counter += 1
    print("Releasing thread lock for item %d!" % item)


for x in range(num_threads):
    print("Daemonizing Thread %d..." % x)
    worker = Thread(target=process_item, args=(x,))
    worker.setDaemon(True)
    worker.start()
    print("Thread %d Daemonized!" % x)