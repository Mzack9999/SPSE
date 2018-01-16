#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# Investigate on how you can use Proxy support with:
# - BeautifulSoup
# - Urllib
# - Mechanize (used mechanicalsoup instead)

import requests
from bs4 import BeautifulSoup
import mechanicalsoup

# Defines proxies
proxy_dict = {
    'http': 'http://47.52.231.140:8080',
    'https': 'https://47.52.231.140:8080'
}

# Proxify BeautifulSoup
r = requests.get('http://www.google.it/', proxies = proxy_dict)
bs = BeautifulSoup(r.content, "html.parser")
print('Title: ', bs.title.encode('utf-8'))

# Proxyfy MechanicalSoup
browser = mechanicalsoup.StatefulBrowser()
browser.session.proxies = proxy_dict
rs = browser.open('http://www.google.it/', verify=False)
print('Data: ', rs)
