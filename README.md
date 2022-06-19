# The WhatsApp BOT
## Setup the environment for WhatsApp business API:
### Setup WhatsApp Cloud API for your account
References this link: https://developers.facebook.com/docs/whatsapp/cloud-api/get-started

### Setup the server
1. Create a server and upload "app.js" file on it. Suggestion server: https://glitch.com/

2. Create a ".env" file on server and setup "VERIFY_TOKEN" (random string, can choose anything you want).

### Create content of messages in WhatsApp business Interface:
1. Login to WhatsApp business account using this url: https://business.facebook.com/wa/manage/home/

2. Press "Account tools" option and choose "Message templates"

3. Create the template message you want to send to and follow the steps.

## Setup local variables in "config.ini" file
1. Open "config.ini" and input the "csv_file_name" value.

2. Input the server url to "url" (including "/webhook" in tail of url)

## Setup local variables in ".env" file
1. Create ".env" file

2. Copy 3 lines below (you need to add the corresponding values instead of "BLANKVALUE"):\
```
WHATSAPP_ACCESS_TOKEN=<BLANKVALUE>
FROM_PHONE_NUMBER_ID=<BLANKVALUE>
WEBHOOK_VERIFY_TOKEN=<BLANKVALUE>
```

## Setup all module required
Run the command:
```pip install -r requirements.txt```
## Setup the .CSV file:
1. Open the *.CSV file that you want to save sending and receiving message.

2. Modify the CSV file with the layout below:
```
-----------------------------------------------------------------------------------------
||     DAY    | Time to Send |   MESSAGE   < | <phone number> | ... | <phone number> > ||
|| DD/MM/YYYY |   hh/mm/ss   | <msg name>  < |                | ... |                > ||
|| DD/MM/YYYY |   hh/mm/ss   | <msg name>  < |                | ... |                > ||
                                           ......
|| DD/MM/YYYY |   hh/mm/ss   | <msg name>  < |                | ... |                > ||
-----------------------------------------------------------------------------------------
```

## Run the BOT:
Run the command:
```python3 main.py```
