#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Send plain text emails.
#
#  Author:  Dongdong Tian @ USTC
#  Date:    2014-08-23
#  Revisions:
#    2014-08-23  Dongdong Tian  Initial coding.
#    2015-10-29  Dongdong Tian  Support outlook.
#    2019-05-25  Ziyi Xi  Use ssl for USTC mail.

import sys
import time
import random
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

#  Hosts:
#  =========== ===================== ==========
#  Service     Host                  Port
#  =========== ===================== ==========
#  163         smtp.163.com          25
#  USTC mail   mail.ustc.edu.cn      25
#  Outlook     smtp-mail.outlook.com 587
#  =========== ===================== ==========
#
# Email accout, password, SMTP host and port
sender = "ziyixi@mail.ustc.edu.cn"
passwd = "******"
host = "mail3.ustc.edu.cn"
port = 465

# Email address of different earthquake data center
recipient = "breq_fast@iris.washington.edu"  # IRIS BREQ_FAST
# recipient = 'autodrm@seismo.nrcan.gc.ca'    # Canada AutoDRM

# DO NOT MODIFY BELOW.
if len(sys.argv) == 1:
    sys.exit("Usage: python %s mailfiles ..." % sys.argv[0])

print("Total %d mails to send!" % len(sys.argv[1:]))
count = 0
for mail in sys.argv[1:]:
    with open(mail) as f:
        msg = MIMEText(f.read())

    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = f"Email automatically sent by Python {mail}"

    with SMTP_SSL(host=host, port=port) as smtp:
        smtp.set_debuglevel(0)
        smtp.ehlo()
        smtp.login(sender, passwd)
        smtp.sendmail(sender, [recipient], msg.as_string())

    count += 1
    print("{}/{}: {} is sent.".format(count, len(sys.argv[1:]), mail))
    # sleep some time
    if count < len(sys.argv[1:]):
        time.sleep(3)
