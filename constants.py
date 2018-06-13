import os

from datetime import date

EMAIL_ADDRESS = 'Predictions Russia 2018 <hello@prode.com>'

PARTICIPANTS_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/11cWCvKKpMgipz2Lrw-medLg8ZPDhaSkRC-FlLBm-ePg/edit#gid=0'
PARTICIPANTS_RANGE_NAME = 'Hoja 1!a2:k'

POSITIONS_SPREADSHEET_URL = 'https://docs.google.com/spreadsheets/d/1G6YWsskdMQR7TxTU_Qk158jkXrG61tnfbVX7a7RTmRg/edit#gid=0'
POSITIONS_RANGE_NAME = 'Hoja 1!a2:b'

LIM_DAY = 10
LIM_MONTH = 'June'

FIRST_PRIZE = 1000
SECOND_PRIZE = 1000
THIRD_PRIZE = 1000

WELCOME_EMAIL_SUBJECT = 'Welcome!'
RECEIVED_EMAIL_SUBJECT = "We've received your predictions"
KICKOFF_EMAIL_SUBJECT = "It's on!"
CLOSE_EMAIL_SUBJECT = "It's over"
FOLLOW_UP_EMAIL_SUBJECT = 'Stadings at {}'.format(date.today())
PAY_RECORDATORY_EMAIL_SUBJECT = "Don't miss the challenge!"
FILE_RECORDATORY_EMAIL_SUBJECT = "Don't forget to send you predictions!"

FILE_NAME = 'Rusia 2018 Predictions.xlsx'
PREDICTIONS_FILE_NAME = 'Seguimiento.xlsx'
