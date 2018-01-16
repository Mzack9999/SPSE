#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Explore http://seleniumhq.org/support/
# - Can you automate the current example in it

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://www.google.com")
elem = driver.find_element_by_name("q")
elem.send_keys("defcon")
elem.send_keys(Keys.RETURN)
driver.close()