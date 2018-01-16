#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# Create a Multi-Threaded Web Spider which
# - Takes a website and depth of spidering as input
# - Download the HTML files only
# - Inserts the HTML into a MySQL Database
# - Design the Schema
# - *It also parses the Forms on each page
# - *inserts into DB with details of Form fields

import requests
import argparse
import sqlite3
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
from urllib.parse import urlparse

# Command line args
parser = argparse.ArgumentParser(description='Multi-Threaded Web Spider')
parser.add_argument('-w', '--website', default='https://stackoverflow.com', help='Website to spider.', required=True)
parser.add_argument('-d', '--depth', type=int, default=1, help='Spidering depth.', required=True)
args = parser.parse_args()


# sql-lite
# pages (title, url, html)
# forms (id-page, form-name)
# form_fields(id-form, field-type, field-value)
# Dummy version holds everything in memory and then store in ad-hoc db
def create_db():
    conn = sqlite3.connect('db.sqllite')
    c = conn.cursor()

    # Create tables
    tables = {
        'page': {'id': 'integer', 'title': 'string', 'url': 'string', 'html': 'string'},
        'form': {'id': 'integer', 'id_page': 'integer', 'form_name': 'string'},
        'form_field': {'id': 'integer', 'type': 'string', 'value': 'string'}
    }
    for table, fields in tables.items():
        command = 'CREATE TABLE ' + table + '(' 
        command += ", ".join(['{nf} {ft}'.format(nf=field_name, ft=field_type) for field_name, field_type in fields.items()])  
        command += ')'
        print(command)
        c.execute(command)
  
    conn.commit()
    conn.close()


def parse_url(url):
    parse_result = urlparse(url)
    return parse_result.scheme and parse_result.netloc


def is_ascii(url):
    try: 
        url.encode('ascii')
    except UnicodeEncodeError: 
        return False
    return True


def handle_page(url, html):
    conn = sqlite3.connect('db.sqllite')
    c = conn.cursor()
    command = 'INSERT INTO page(url, html) VALUES(?, ?)'
    c.execute(command, (url, html))
    conn.commit()
    conn.close()


def crawl_url(q):
    while True:
        url, current_depth = q.get()
        if current_depth > depth or not is_ascii(url) or not parse_url(url):
            continue
        # Get url
        print('Current url: ', str(url), 'Depth: ', current_depth)
        r = requests.get(url)
        bs = BeautifulSoup(r.content, 'html.parser')
        handle_page(url, bs.html.prettify())
        # Add new links
        for x in bs.find_all('a', href=True):
            q.put((x.get('href'), current_depth + 1))
        q.task_done()


num_threads = 10

print("Creating queue...")
q = Queue()

for x in range(num_threads):
    print("Daemonizing Thread %d..." % x)
    worker = Thread(target=crawl_url, args=(q, ))
    worker.setDaemon(True)
    worker.start()
    print("Thread %d Daemonized!" % x)

# Start to crawl recursively pages
print("Populating queue....")
base_url = args.website
depth = args.depth
q.put((base_url, 1))
q.join()

