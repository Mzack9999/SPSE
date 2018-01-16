#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Read /var/log/messages
# - Filter and print only messages about USB

with open("/var/log/messages", "r") as f:
    for line in f:
        if "usb" in line:
            print(line)