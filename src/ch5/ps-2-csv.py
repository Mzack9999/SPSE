#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Write the list of processes in a CSV file
# - The first row should be the table column names

import immblib
import csv


def main(args):

    imm = immlib.Debugger()
    processes = imm.ps()
    headers = ['PID', 'Name', 'Path', 'Services']
    with open('processes.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(processes)

    return '[+] Process dump finished'

