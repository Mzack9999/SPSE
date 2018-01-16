#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - In the example shown we did not try and modify the hidden fields. Try to see how you can do it and send arbitrary data

import mechanicalsoup

br = mechanicalsoup.StatefulBrowser()
br.open('http://www.example.example/form.htm')

br.select_form(nr=0)
br['Name'] = 'John'
br['Surname'] = 'Doe'
# Hidden Field
br['price'] = 0
br.submit_selected()

print(br.get_current_page())