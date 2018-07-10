# =============================================================================
#          File: mails.py
#        Author: Andre Brener
#       Created: 14 Jun 2017
# Last Modified: 10 Jul 2018
#   Description: description
# =============================================================================
import os
import sys
import logging
import logging.config

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

CURRENT_DIR_LIST = CURRENT_DIR.split(os.sep)

PROJECT_DIR = os.path.join(
    os.sep, *CURRENT_DIR_LIST[:CURRENT_DIR_LIST.index('close_mail')]
)

sys.path.append(PROJECT_DIR)

import pandas as pd

from mails import send_mail
from config import config
from constants import (
    CLOSE_EMAIL_SUBJECT, EMAIL_ADDRESS, PARTICIPANTS_RANGE_NAME,
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
    def __init__(
        self, name, email, first_winner, second_winner, third_winner, templates
    ):
        self.name = name
        self.email = email
        self.first_winner = first_winner
        self.second_winner = second_winner
        self.third_winner = third_winner
        self.participants = []
        self.user_template = templates['mail_body.html']

    def render(self):
        return self.user_template.render(
            name=get_only_name(self.name),
            participants=self.participants,
            first_winner=self.first_winner,
            second_winner=self.second_winner,
            third_winner=self.third_winner
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


def prepare_mail(user, templates):
    mail_to = user.email
    mail_subject = CLOSE_EMAIL_SUBJECT
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
            result_dict[sn] = [int(df.ix[2, 8])]

    df = pd.DataFrame(result_dict).T.reset_index()
    df.columns = ['name', 'score']
    df = df.sort_values('score', ascending=False)

    winners_df = df.head(3)

    second_winner = 'No hay segundo premio'
    third_winner = 'No hay tercer premio'

    winner_scores = winners_df['score'].tolist()
    winner_names = winners_df['name'].tolist()

    if len(set(winner_scores)) == winners_df.shape[0]:
        first_winner = winner_names[0]
        second_winner = winner_names[1]
        third_winner = winner_names[2]

    elif len(set(winner_scores)) == 1:
        first_winner = winner_names[0] + ' & ' + winner_names[
            1
        ] + ' & ' + winner_names[2]

    elif winner_scores[0] == winner_scores[1]:
        first_winner = winner_names[0] + ' & ' + winner_names[1]
        second_winner = winner_names[2]

    elif winner_scores[1] == winner_scores[2]:
        first_winner = winner_names[0]
        second_winner = winner_names[1] + ' & ' + winner_names[2]

    df['first_winner'] = first_winner
    df['second_winner'] = second_winner
    df['third_winner'] = third_winner

    return df


def send_close_mail():

    part_df = get_participants(
        PARTICIPANTS_SPREADSHEET_URL, PARTICIPANTS_RANGE_NAME
    )

    part_df['name'] = part_df['first_name'] + ' ' + part_df['surname']

    pos_df = get_positions()

    df = pd.merge(pos_df, part_df)

    df['position'] = df.index + 1

    test = pos_df[~pos_df['name'].isin(df['name'])]

    if not test.empty:
        logger.info("These participants are missing")
        print(test)

        sys.exit()

    usrs = get_object_list(
        User, df, 'name',
        ['email', 'first_winner', 'second_winner', 'third_winner'], TEMPLATES
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
        # sys.exit()

        send_mail([mail_to], mail_subject, mail_body)


if __name__ == '__main__':
    logging.config.dictConfig(config['logger'])
    send_close_mail()
