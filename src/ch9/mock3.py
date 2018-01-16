#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Write a simple web crawler which fetch the robots.txt file of a website
# - run your crawler on the top 1000 sites a ranked by Alexa
# - report on the top 40 directory names which are disallowed for robots

import concurrent.futures
import requests
import csv
from collections import OrderedDict


def multithreading(func, args, workers):
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def parse_robot_file(url):
    global disallowed_dirs
    print('https://' + url + '/robots.txt')
    r = requests.get('https://' + url + '/robots.txt')
    if r.status_code != 200:
        return False
    for directory in r.text.splitlines():
        disallowed_dirs[directory] += 1


disallowed_dirs = {}
args_list = []
with open('top1m.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        args_list.append(row[2])
multithreading(parse_robot_file, args_list, 10)
top_folders = OrderedDict(sorted(disallowed_dirs.items(), key=lambda t: t[1]))
for k, _ in top_folders:
    print(k)
