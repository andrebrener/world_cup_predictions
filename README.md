# 2018 World Cup Prediction Game

This application is used to organize a prediction game for the Russia 2018 World Cup.

## How does it work?
- Send welcome email to participants in [database](https://docs.google.com/spreadsheets/d/11cWCvKKpMgipz2Lrw-medLg8ZPDhaSkRC-FlLBm-ePg/edit#gid=0).
- Set the `sent_preds` column in the [database](https://docs.google.com/spreadsheets/d/11cWCvKKpMgipz2Lrw-medLg8ZPDhaSkRC-FlLBm-ePg/edit#gid=0) to 1 when you receive the complete file from the participant.
- Send file recordatory email to remind users in database to send their predictions.
- Send pay recordatory email to remind users in database to make their payment.
- Set the `paid` column in the [database](https://docs.google.com/spreadsheets/d/11cWCvKKpMgipz2Lrw-medLg8ZPDhaSkRC-FlLBm-ePg/edit#gid=0) to 1 when you receive the payment from the participant.
- Send the kickoff mail when it's ready to start.
- Update the [standings](https://docs.google.com/spreadsheets/d/1G6YWsskdMQR7TxTU_Qk158jkXrG61tnfbVX7a7RTmRg/edit#gid=0) and send the follow up mail when you want to inform the standings up to date.
- Send the close mail to finish the game and inform winners & their respective prizes.

## The prediction file
The Excel file has 3 spreadsheets:
- `Rules`: it explains in detail how each participant sums points in the game.
- `My Prediction`: the participant must fill this spreadsheet with their predictions.
- `Results`: this spreadsheet is to keep track of the points earned. By completing it with actual results, the predictions spreadsheet will be updated with the score.


## Getting Started

### 1. Clone Repo

`git clone https://github.com/andrebrener/world_cup_predictions`

### 2. Install Packages Required

Go in the directory of the repo and run:
```pip install -r requirements.txt```

### 3. Generate Google Credentials
You will need credentials for google drive & gmail. For this you have to:
- Create a file in the repo called `google_credentials.py` where you name the variables `GOOGLE_PASS` and `GOOGLE_USERNAME`.
- Generate credentials for [Google Spreadsheet](https://console.developers.google.com/flows/enableapi?apiid=sheets.googleapis.com&pli=1) and save the file called `client_secret.json` in the repo directory.
- Enable gmail access to non secure apps. For more info read this [tutorial](https://support.google.com/cloudidentity/answer/6260879?hl=en).

### 4. Build Database in Google Spreadsheets
You will need to create 2 spreadsheets:
- The [participants databese](https://docs.google.com/spreadsheets/d/11cWCvKKpMgipz2Lrw-medLg8ZPDhaSkRC-FlLBm-ePg/edit#gid=0). You will see that it will be updated automatically as the mails are sent. The columns in green are only ones that have to be updated manually.
- The [standings](https://docs.google.com/spreadsheets/d/1G6YWsskdMQR7TxTU_Qk158jkXrG61tnfbVX7a7RTmRg/edit?usp=drive_web&ouid=110894318773281496189). This file will have to be updated manually when the follow up mail needs to be sent.

### 5. Insert Constants
In [constants.py](https://github.com/andrebrener/world_cup_predictions/blob/master/constants.py) you can define:
- `EMAIL_ADDRESS`: The email address that will be sending the emails.
- `PARTICIPANTS_SPREADSHEET_URL`: The participants database spreadsheet url.
- `PARTICIPANTS_RANGE_NAME`: The cells range in the participants spreadsheet. This must be left as it is unless you want to add some more features.
- `POSITIONS_SPREADSHEET_URL`: The standings spreadsheet url.
- `POSITIONS_RANGE_NAME`: The cells range in the standings spreadsheet. This must be left as it is unless you want to add some more fea
- `LIM_DAY`: Day limit to register.
- `LIM_MONTH`: Month limit to register.
- `FIRST_PRIZE`: First prize value.
- `SECOND_PRIZE`: Second prize value.
- `THIRD_PRIZE`: Third prize value.
- `WELCOME_EMAIL_SUBJECT`: Email subject to welcome.
- `RECEIVED_EMAIL_SUBJECT`: Email subject to notifiy the reception of the file.
- `KICKOFF_EMAIL_SUBJECT`: Email subject to send when the registration is closed and it's all set.
- `CLOSE_EMAIL_SUBJECT`: Email subject to close the game and inform winners.
- `FOLLOW_UP_EMAIL_SUBJECT`: Email subject to notify the standings up to date.
- `PAY_RECORDATORY_EMAIL_SUBJECT`: Email subject to remind participants to make the payment.
- `FILE_RECORDATORY_EMAIL_SUBJECT`: Email subject to remind participants to send the predictions' file.
- `FILE_NAME`: Name of the attached file. This must be left as it is unless another file is used.


