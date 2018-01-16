#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - If you try and download a very large file, then how do you monitor the progress?
# - Research on urllib.urlretrieve() to solve this problem

# Using requests instead of urllib

import requests
import tqdm


def download_file(remote_file, local_file, chunk_size = 1024):
    r = requests.get(remote_file, stream=True)
    remote_file_lenght = int(r.headers.get('content-length'))
    with open(local_file, 'wb') as f:
        for chunk in tqdm.tqdm(r.iter_content(chunk_size=chunk_size), total=(remote_file_lenght/chunk_size + 1)):
            if chunk:
                f.write(chunk)
                f.flush()


download_file('https://dl.google.com/chrome/mac/stable/GGRO/googlechrome.dmg', '/tmp/googlechrome.dmg')
