#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Create a automated email parser-when email is received in your account, this scrupt will automatically be triggered,
#   it will then separate the attachments, store them, and upload them to online virus scan sites
# - it will then forward the email to you if the online scans give a green signal

import imaplib
import email
import os
import hashlib
from virus_total_apis import PublicApi as VirusTotalPublicApi


def handle_attachment(file_name):
    with open(file_name, 'rb') as file:
        file_data = file.read()
    file_md5 = hashlib.md5(file_data).hexdigest()

    api_key = 'Sign-Up for API Key at virustotal.com'
    vt = VirusTotalPublicApi(api_key)

    response = vt.get_file_report(file_md5)
    return response['results']['positives'] > 0


imaplib.IMAP4.debug = imaplib.IMAP4_SSL.debug = 1

host, username, password = ('host', 'username', 'password')

con = imaplib.IMAP4_SSL(host, 993)
con.login(username, password)
con.select()
typ, data = con.search(None, '(UNSEEN)')
for num in data[0].split():
    typ, data = con.fetch(num, '(RFC822)')
    text = data[0][1]
    msg = email.message_from_string(text)
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        data = part.get_payload(decode=True)
        if not data:
            continue
        with open(os.join(os.environ['HOME'], filename), 'w') as f:
            f.write(data)
        scan_result = handle_attachment(filename)
        print('Scan {f} result: {b}'.format(f=filename, b=scan_result))

con.close()
con.logout()
