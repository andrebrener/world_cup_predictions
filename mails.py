# =============================================================================
#          File: mails.py
#        Author: Andre Brener
#       Created: 13 Jun 2017
# Last Modified: 11 May 2018
#   Description: description
# =============================================================================
import os
import logging
import smtplib

from time import sleep
from email.utils import COMMASPACE
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import jinja2

from constants import EMAIL_ADDRESS
from google_credentials import GOOGLE_PASS, GOOGLE_USERNAME

logger = logging.getLogger('main_logger.' + __name__)


def render(tpl_path, context):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')
                              ).get_template(filename).render(context)


def send_mail(send_to, subject, mail_body, files=None):

    try:
        user_address, password = GOOGLE_USERNAME, GOOGLE_PASS
    except (FileNotFoundError):
        user_address = os.environ.get('SES_ACCESS_KEY_ID', None)
        password = os.environ.get('SES_SECRET_ACCESS_KEY', None)

    from_address = EMAIL_ADDRESS
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = COMMASPACE.join(send_to)
    msg['Subject'] = subject
    msg.attach(MIMEText(mail_body.encode('utf-8'), 'html', 'utf-8'))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(fil.read(), Name=os.path.basename(f))
            part['Content-Disposition'] = \
                'attachment; filename="%s"' % os.path.basename(f)
            msg.attach(part)

    tries = 1
    while tries < 30:
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(user_address, password)
                server.sendmail(from_address, send_to, msg.as_string())
                logger.info("Email sent to {} :)".format(send_to[0]))
                break
        except Exception as e:
            logger.error("Mail failed. ERROR: {}".format(e))
            tries += 1
            sleep(70 * tries)


def send_customized_mail(
    df,
    to_send_df,
    spreadsheet_url,
    range_name,
    current_dir,
    mail_subject,
    context,
    files=None
):

    if to_send_df.empty:
        logger.info('No user to send email to')
        return None

    for row in to_send_df.iterrows():
        row_data = row[1]
        name = row_data['name'].split()[0]
        mail_to = row_data['email']
        mail_dir = os.path.join(current_dir, 'mail_body.html')
        context['name'] = name
        mail_body = render(mail_dir, context)

        send_mail([mail_to], mail_subject, mail_body, files=files)
