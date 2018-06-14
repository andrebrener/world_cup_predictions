# =============================================================================
#          File: mails.py
#        Author: Andre Brener
#       Created: 14 Jun 2017
# Last Modified: 14 Jun 2018
#   Description: description
# =============================================================================
import os
import sys
import logging
import logging.config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR_LIST = CURRENT_DIR.split(os.sep)

PROJECT_DIR = os.path.join(
    os.sep, *CURRENT_DIR_LIST[:CURRENT_DIR_LIST.index('follow_up_mail')]
)

sys.path.append(PROJECT_DIR)

import pandas as pd

from mails import send_mail
from config import config
from constants import (
    EMAIL_ADDRESS, FOLLOW_UP_EMAIL_SUBJECT, PARTICIPANTS_RANGE_NAME,
    PARTICIPANTS_SPREADSHEET_URL, PREDICTIONS_FILE_NAME
)
from jinja_customs import load_templates
from get_gdrive_data import get_participants
from google_credentials import GOOGLE_PASS, GOOGLE_USERNAME

os.chdir(PROJECT_DIR)

logger = logging.getLogger('main_logger')

TEMPLATES_DIR = CURRENT_DIR + '/mail_templates'

TEMPLATES = load_templates(TEMPLATES_DIR)


class User:
    def __init__(self, name, email, support_message, templates):
        self.name = name
        self.email = email
        self.support_message = support_message
        self.participants = []
        self.user_template = templates['mail_body.html']

    def render(self):
        return self.user_template.render(
            name=get_only_name(self.name),
            participants=self.participants,
            support_message=self.support_message
        )


class Participant:
    def __init__(self, name, points, position, templates):
        self.name = name
        self.points = points
        self.position = position
        self.coin_template = templates['participant_mail.html']

    def render(self):
        return self.coin_template.render(
            name=self.name, position=self.position, points=self.points
        )


def get_only_name(full_name):
    name_list = full_name.split()
    return name_list[0]


def get_support_message(position):
    if position == 1:
        return 'A mantener esa diferencia!'
    elif position < 8:
        return 'Falta mucho, todavía podes alcanzar a los de arriba!'
    else:
        return 'Nada'


def prepare_mail(user, templates):
    mail_to = user.email
    mail_subject = FOLLOW_UP_EMAIL_SUBJECT
    mail_body = user.render()
    return mail_to, mail_subject, mail_body


def get_object_list(cls, df, main_col, columns, templates):
    return [
        cls(i, *[j[col] for col in columns], templates)
        for i in df[main_col].unique()
        for j in [df[df[main_col] == i][columns].iloc[0]]
    ]


def get_positions():

    excel_dict = pd.read_excel(
        PREDICTIONS_FILE_NAME, sheet_name=None, header=None
    )

    result_dict = {}
    for sn, df in excel_dict.items():
        if len(sn) > 5 and sn not in ['Reglamento', 'Resultados Reales']:
            result_dict[sn] = [df.ix[2, 8]]

    df = pd.DataFrame(result_dict).T.reset_index()
    df.columns = ['name', 'score']

    return df


def send_follow_up_mail():

    part_df = get_participants(
        PARTICIPANTS_SPREADSHEET_URL, PARTICIPANTS_RANGE_NAME
    )

    part_df['name'] = part_df['first_name'] + ' ' + part_df['surname']

    pos_df = get_positions()

    df = pd.merge(pos_df, part_df)

    df['support_message'] = df['position'].apply(get_support_message)

    usrs = get_object_list(
        User, df, 'name', ['email', 'support_message'], TEMPLATES
    )

    for usr in usrs:
        participants = get_object_list(
            Participant, df, 'name', ['score', 'position'], TEMPLATES
        )

        usr.participants = participants

    for usr in usrs:
        mail_to, mail_subject, mail_body = prepare_mail(usr, TEMPLATES)

        # with open('html_example.html', 'w') as f:
        # f.write(mail_body)

        send_mail([mail_to], mail_subject, mail_body)
        print('email sent to {}'.format(mail_to))


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    send_follow_up_mail()
