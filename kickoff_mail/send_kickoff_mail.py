import os
import sys
import logging
import logging.config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR_LIST = CURRENT_DIR.split(os.sep)

PROJECT_DIR = os.path.join(
    os.sep, *CURRENT_DIR_LIST[:CURRENT_DIR_LIST.index('kickoff_mail')]
)

sys.path.append(PROJECT_DIR)

from mails import send_customized_mail, send_mail
from config import config
from constants import (
    FIRST_PRIZE, KICKOFF_EMAIL_SUBJECT, PARTICIPANTS_RANGE_NAME,
    PARTICIPANTS_SPREADSHEET_URL, SECOND_PRIZE, THIRD_PRIZE
)
from get_gdrive_data import get_participants
from gdrive_connector import update_spreadsheet

os.chdir(PROJECT_DIR)


def send_kickoff_mail():

    df = get_participants(
        PARTICIPANTS_SPREADSHEET_URL, PARTICIPANTS_RANGE_NAME
    )

    to_send_df = df[(df['kickoff_mail'] == 0) & (df['sent_preds'] > 0) &
                    (df['paid'] > 0)]

    context = {
        'first_prize': FIRST_PRIZE,
        'second_prize': SECOND_PRIZE,
        'third_prize': THIRD_PRIZE
    }

    send_customized_mail(
        df,
        to_send_df,
        PARTICIPANTS_SPREADSHEET_URL,
        PARTICIPANTS_RANGE_NAME,
        CURRENT_DIR,
        KICKOFF_EMAIL_SUBJECT,
        context,
        files=None
    )

    update_spreadsheet(
        df, to_send_df, 'kickoff_mail', PARTICIPANTS_SPREADSHEET_URL,
        PARTICIPANTS_RANGE_NAME
    )


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])

    send_kickoff_mail()
