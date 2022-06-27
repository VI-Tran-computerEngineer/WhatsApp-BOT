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
## Setup the database:
1. Open MySQL and create new database


2. Open "config.ini" and modify the MySQL parameters, include hostname, username, password, database name

3. Create new table contains the information of the phone number to send the message and the key is only to the table containing the daily message delivery schedule. The table contains 2 columns whose names are "phone_number" and "msg_sent_schedule" respectively.
```
--------------------------------------------------
||     phone_number    	|   msg_sent_schedule 	||
|| 	 <string>	| 	 <string>	||
|| 	 <string>	| 	 <string>	||
                     ......
|| 	 <string>	|  	 <string>	||
--------------------------------------------------
```

4. Open "config.ini" and modify the "to_phone_table" parameter by table name.

5. Create tables contains the sending schedule as the layout and columns name below. The table name is the value of "msg_sent_schedule" column of the table above
```
--------------------------------------------------
||     sending_time    	|   	msg_name	||
|| 	 <HH:MM>	| 	 <HH:MM>	||
|| 	 <HH:MM>	| 	 <HH:MM>	||
                     ......
|| 	 <HH:MM>	| 	 <HH:MM>	||
--------------------------------------------------
```

6. Create the table contains replied message. It must contain 4 columns name "datetime", "phone_number", "sent_msg",	"replied_msg".	
```
------------------------------------------------------------------
||     	datetime    	| phone_number | sent_msg | replied_msg ||
|| DD/mm/YYYY HH:MM:SS	|   <string>   | <string> |   <string> 	||
|| DD/mm/YYYY HH:MM:SS	|   <string>   | <string> |   <string> 	||
                     		......
|| DD/mm/YYYY HH:MM:SS	|   <string>   | <string> |   <string> 	||
------------------------------------------------------------------
```

7. Open "config.ini" and modify the "replied_msg_table" parameter by table name.

## Run the BOT:
Run the command:
```python3 main.py```

## Some supported command for MySQL:
1. Create the new table:
```
CREATE TABLE <table_name> (
    <column_name> <DATA TYPE>,
    ....
)

"""Example for creating table named "to_phone_number":
CREATE TABLE to_phone_number (
phone_number VARCHAR(255), 
msg_sent_schedule VARCHAR(255)
)

"""
```

2. Add new column into table
```
INSERT INTO <table_name> (<column_name>,...)
VALUES (<value>,...)

"""Example for adding new row into "to_phone_number" table:
INSERT INTO to_phone_number (phone_number, msg_sent_schedule)
VALUES ("123456789", "schedule_for_US_timezone")

"""
```

3. Modify the specific row in table
```
UPDATE <table_name>
SET <column_name>=<changed_value>,...
WHERE <column_name>=<?>

"""Example for updating schedule of phone_number "123456789":
UPDATE to_phone_number
SET msg_sent_schedule="schedule_for_VN_timezone",...
WHERE phone_number="123456789"
"""
```

4. Delete the specific row in table
```
DELETE FROM <table_name>
WHERE <condition>,...

"""Example for deleting the phone_number is "123456789" on "to_phone_number" column:
DELETE FROM to_phone_number
WHERE phone_number="123456789"
"""
```
