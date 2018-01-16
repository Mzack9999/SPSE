#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Explore the concept of mechanize.CookieJar
# - Why is it useful?
# - Sample code to illustrate its functionality

import pickle
import requests
import mechanicalsoup
from http import cookiejar

c = cookiejar.CookieJar()
s = requests.Session()
s.cookies = c

br1 = mechanicalsoup.StatefulBrowser(session=s)

br1.open('http://spse_dvwa_1/')
# Login
br1.select_form(nr=0)
br1['username'] = "admin"
br1['password'] = "password"
br1.submit_selected()

# Dump session
pickle.dump(br1, open("browser.obj", 'wb'))

# Reload session into second mechanicalsoup instance
br2 = pickle.load(open("browser.obj", 'rb'))
br2.follow_link(br2.find_link(text='SQL Injection'))
print(br2.get_current_page())