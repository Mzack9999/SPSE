#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Urlencode() does a bad job in handling special characters in the URL
# - Research on .quote() and .quote_plus() and illustrate how they can help

import urllib.parse

# .quote() example
# Replace special characters in string using the %xx escape. Letters, digits, and the characters '_.-' are never quoted
print(".quote() example: ", urllib.parse.quote("châteu-- /", safe=''))

# .quote_plus() example
# Like quote(), but also replace spaces by plus signs, as required for quoting HTML form values 
# when building up a query string to go into a URL. 
# Plus signs in the original string are escaped unless they are included in safe. 
# It also does not have safe default to '/'
print(".quote() example: ", urllib.parse.quote_plus("châteu-- /", safe=''))