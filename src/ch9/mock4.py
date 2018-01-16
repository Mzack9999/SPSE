#!/usr/bin/env python

# Author: SPSE-3232
# Purpose:
# - Write a IMAP Client script which can download all the email from a IMAP server and store them in a Sqlite DB locally
# - we will provide IP and Auth details

import sqlite3
import imaplib
import email


def create_db():
    conn = sqlite3.connect('db.sqllite')
    c = conn.cursor()

    # Create tables
    tables = {
        'mails': {'id': 'integer', 'from': 'string', 'text': 'string', 'date': 'string', 'subject': 'string'},
    }
    for table, fields in tables.items():
        command = 'CREATE TABLE ' + table + '('
        command += ", ".join(
            ['{nf} {ft}'.format(nf=field_name, ft=field_type) for field_name, field_type in fields.items()])
        command += ')'
        print(command)
        c.execute(command)

    conn.commit()
    conn.close()


create_db()

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('myusername@gmail.com', 'mypassword')
mail.list()
mail.select("inbox")
type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

for i in range(latest_email_id,first_email_id, -1):
    typ, data = mail.fetch(i, '(RFC822)' )
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            email_subject = msg['subject']
            email_from = msg['from']
            email_body = msg['body']
            email_date = msg['date']
            conn = sqlite3.connect('db.sqllite')
            c = conn.cursor()
            command = 'INSERT INTO mails(from, text, date, subject) VALUES(?, ?, ?, ?)'
            c.execute(command, (email_from, email_body, email_date, email_subject))
            conn.commit()
            conn.close()