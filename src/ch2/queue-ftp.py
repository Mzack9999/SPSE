#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a list of ftp sites
# - Create a WorkerThread and Queue which can login to these sites and list the root directory and exit
# - Use 5 threads for this job and 10 ftp sites

from Queue import Queue
from threading import Thread
import ftplib


ftp_list = [
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
    'debian.org',
]


def work_thread(q):
    while True:
        item = q.get()
        print("Working on item: ", item)
        f = ftplib.FTP(host = item)
        f.login()
        ls = []
        f.retrlines('MLSD', ls.append)
        for l in ls:
            print(l)
        q.task_done()


print("Creating queue...")
q = Queue()
num_threads = 5

print("Populating queue...")
for x in ftp_list:
    print("Inserting: ", x)
    q.put(x)

for x in range(num_threads):
    print("Daemonizing Thread %d..." % x)
    worker = Thread(target=work_thread, args=(q,))
    worker.setDaemon(True)
    worker.start()
    print("Thread %d Demonized!" % x)

print("Waiting worker threads to join...")
q.join()
print("All workers terminated!")