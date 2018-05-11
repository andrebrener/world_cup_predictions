import os
import sys
import logging
import logging.config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR_LIST = CURRENT_DIR.split(os.sep)

PROJECT_DIR = os.path.join(
    os.sep, *CURRENT_DIR_LIST[:CURRENT_DIR_LIST.index('file_recordatory_mail')]
)

sys.path.append(PROJECT_DIR)

from mails import send_customized_mail, send_mail
from config import config
from constants import (
    FILE_NAME, FILE_RECORDATORY_EMAIL_SUBJECT, LIM_DAY, LIM_MONTH,
    PARTICIPANTS_RANGE_NAME, PARTICIPANTS_SPREADSHEET_URL
)
from get_gdrive_data import get_participants
from gdrive_connector import update_spreadsheet

os.chdir(PROJECT_DIR)


def send_file_recordatory_mail():

    df = get_participants(
        PARTICIPANTS_SPREADSHEET_URL, PARTICIPANTS_RANGE_NAME
    )

    to_send_df = df[(df['welcome_mail'] > 0) & (df['sent_preds'] == 0)]

    context = {'lim_day': LIM_DAY, 'lim_month': LIM_MONTH}

    file_dir = os.path.join(PROJECT_DIR, FILE_NAME)

    send_customized_mail(
        df,
        to_send_df,
        PARTICIPANTS_SPREADSHEET_URL,
        PARTICIPANTS_RANGE_NAME,
        CURRENT_DIR,
        FILE_RECORDATORY_EMAIL_SUBJECT,
        context,
        files=[file_dir]
    )

    update_spreadsheet(
        df, to_send_df, 'file_recordatory_mail', PARTICIPANTS_SPREADSHEET_URL,
        PARTICIPANTS_RANGE_NAME
    )


if __name__ == '__main__':

    logging.config.dictConfig(config['logger'])
    send_file_recordatory_mail()
