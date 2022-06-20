from whatsapp_interaction import WhatsApp_API
from csv_lib import get_data_from_csv, check_available_timestamp, save_msg_to_csv
import time
import threading
from os import getenv
from dotenv import load_dotenv
import configparser

# Get values from .ini file
config = configparser.ConfigParser()
config.read('config.ini')
CSV_FILE_NAME = config['csv']['csv_file_name']
# Get enviroment variables
load_dotenv()
ACCESS_TOKEN = getenv('WHATSAPP_ACCESS_TOKEN')
FROM_PHONE_NUMBER_ID = getenv('FROM_PHONE_NUMBER_ID')
WEBHOOK_VERIFY_TOKEN = getenv('WEBHOOK_VERIFY_TOKEN')
WEBHOOK_URL = config['webhook']['url']  # + "/" + WEBHOOK_VERIFY_TOKEN

WAITING_SENT_INTERVAL = int(config['system']['waiting_sent_interval'])
WAITING_RECV_INTERVAL = int(config['system']['waiting_received_interval'])


class WhatsApp_user_callback:
    def __init__(self, from_phone_number_id, access_token, webhook_url):
        self.whatsapp_api = WhatsApp_API(
            from_phone_number_id, access_token, webhook_url)
        self.send_msgs_dict = get_data_from_csv(CSV_FILE_NAME)
        self.send_msgs_done = False

    def send_preschedule_msgs(self):
        if self.done_the_bot():
            print("No more msg need to send!")
            return
        to_phone_numbers = list(self.send_msgs_dict.keys())
        while True:
            for phone_number in to_phone_numbers:
                if len(self.send_msgs_dict[phone_number]) == 0:
                    del self.send_msgs_dict[phone_number]
                    to_phone_numbers.remove(phone_number)
                    continue
                # if sent the msg before ==> ignore the phone number
                if self.send_msgs_dict[phone_number][0]["sent"]:
                    continue
                send_timestamp = self.send_msgs_dict[phone_number][0]["time"]
                msg = self.send_msgs_dict[phone_number][0]["body"]
                if (
                    check_available_timestamp(send_timestamp) == "ontime"
                    or check_available_timestamp(send_timestamp) == "overtime"
                ):
                    self.whatsapp_api.send_message(phone_number, msg)
                    self.send_msgs_dict[phone_number][0]["sent"] = True
            if self.done_the_bot():
                print("No more msg need to send!")
                return
            time.sleep(WAITING_SENT_INTERVAL)

    def wait_4_msgs_received(self):
        while True:
            received_msgs = self.whatsapp_api.get_messages_received()
            if received_msgs:
                for recv_msg in received_msgs["data"]:
                    from_phone_number = recv_msg["from"]
                    recved_msg = recv_msg["body"]
                    print(f"Received message from {from_phone_number}!")
                    send_msg = self.send_msgs_dict[from_phone_number][0]["body"]
                    save_msg_to_csv(
                        CSV_FILE_NAME, from_phone_number, send_msg, recved_msg)
                    self.send_msgs_dict[from_phone_number].pop(0)
                received_msgs = None

            time.sleep(WAITING_RECV_INTERVAL)

    def done_the_bot(self):
        return False if len(self.send_msgs_dict) > 0 else True


def main():
    print("******************************")
    print("*     Starting the BOT       *")
    print("******************************")
    callback = WhatsApp_user_callback(
        FROM_PHONE_NUMBER_ID, ACCESS_TOKEN, WEBHOOK_URL)
    threading.Thread(target=callback.send_preschedule_msgs,
                     daemon=True).start()
    threading.Thread(target=callback.wait_4_msgs_received,
                     daemon=True).start()

    try:
        done_the_bot = callback.done_the_bot()
        while done_the_bot == False:
            done_the_bot = callback.done_the_bot()
            pass
        print("******************************")
        print("*        End the BOT         *")
        print("******************************")
        exit(0)
    except KeyboardInterrupt:
        print("******************************")
        print("*    End the BOT manually    *")
        print("******************************")
        exit(1)


if __name__ == "__main__":
    main()
