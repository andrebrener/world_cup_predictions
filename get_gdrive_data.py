import pandas as pd

from gdrive_connector import get_data


def get_participants(spreadsheet_link, range_name):
    values = get_data(spreadsheet_link, range_name)

    user_dict = {}

    for usr in values:
        user_dict[usr[0]] = usr[1:]

    usr_df = pd.DataFrame(user_dict).T.reset_index()
    usr_df.columns = [
        'id', 'name', 'email', 'phone', 'welcome_mail',
        'file_recordatory_mail', 'sent_preds', 'received_mail',
        'pay_recordatory_mail', 'paid', 'kickoff_mail'
    ]
    for col in [
        'welcome_mail', 'sent_preds', 'received_mail', 'pay_recordatory_mail',
        'paid', 'kickoff_mail'
    ]:
        usr_df[col] = usr_df[col].astype(int)

    return usr_df


if __name__ == '__main__':

    spreadsheet_link = 'https://docs.google.com/spreadsheets/d/1rk8kRGCw4MMkZtgnkFcp-G4sXW5j2tKAnrHl-W5Sqbo/edit#gid=0'

    range_name = 'Hoja 1!a2:k'

    df = get_participants(spreadsheet_link, range_name)

    print(df)
