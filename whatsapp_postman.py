import collections
import time
from datetime import datetime
import configparser

from whatsapp_interaction import WhatsApp_API
from sql_connection import MySQL_connector

# Get values from .ini file
config = configparser.ConfigParser()
config.read('config.ini')
WAITING_SENT_INTERVAL = int(config['system']['waiting_sent_interval'])
WAITING_RECV_INTERVAL = int(config['system']['waiting_received_interval'])


class WhatsApp_user_callback:
    def __init__(self):
        self.whatsapp_api = WhatsApp_API()
        self.sql_connector = MySQL_connector()
        self.send_msgs_dict = self.construct_data()
        self.send_msgs_done = False

    def send_preschedule_msgs(self):

        def sort_list(data_list):
            data_list = collections.deque(data_list)
            data_list.rotate(1)
            return data_list

        def is_next_day(dtime):
            current_day = datetime.now().strftime("%d/%m/%Y")
            if current_day != dtime:
                return True
            return False

        if len(self.send_msgs_dict) == 0:
            print("No msg need to send!")
            return

        to_phone_numbers = list(self.send_msgs_dict.keys())
        send_msgs_done = False
        current_day = None
        while True:
            time.sleep(WAITING_SENT_INTERVAL)
            if send_msgs_done:
                current_day = datetime.now().strftime("%d/%m/%Y")
                if is_next_day(current_day):
                    send_msgs_done = False
                    self.reset_sent_status()
                continue
            for phone_number in to_phone_numbers:
                # if sent the msg before ==> ignore the phone number
                send_msgs = self.send_msgs_dict[phone_number]
                if send_msgs[0]["sent"]:
                    continue
                send_time = send_msgs[0]["time"]
                msg = send_msgs[0]["body"]
                if check_timer_status(send_time) == "ontime":
                    self.whatsapp_api.send_message(phone_number, msg)
                    send_msgs[0]["sent"] = True
                    send_msgs = sort_list(send_msgs)

            send_msgs_done = self.done_the_bot_today()
            if send_msgs_done:
                print("All messages sent today!\nWaiting for tomorrow.......")

    def wait_4_msgs_received(self):
        while True:
            received_msgs = self.whatsapp_api.get_messages_received()
            if received_msgs:
                for recv_msg in received_msgs["data"]:
                    from_phone_number = recv_msg["from"]
                    recved_msg = recv_msg["body"]
                    print(f"Received message from {from_phone_number}!")
                    send_msg_info = self.send_msgs_dict[from_phone_number][0]
                    self.sql_connector.store_reply_to_table(
                        from_phone_number, send_msg_info, recved_msg)
                received_msgs = None

            time.sleep(WAITING_RECV_INTERVAL)

    def done_the_bot_today(self):
        phone_numbers = list(self.send_msgs_dict.keys())
        for phone_number in phone_numbers:
            if self.send_msgs_dict[phone_number][0] == False:
                return False
        return True

    def construct_data(self):
        phone_number_list = self.sql_connector.query_to_phone_number()
        send_msgs_info = {}
        for phone_number, schedule_name in phone_number_list:
            send_msgs_info[phone_number] = []

            msgs_schedule = self.sql_connector.query_msgs_schedule(
                schedule_name)
            for send_time, msg in msgs_schedule:
                sent_or_not = False
                if check_timer_status(send_time) == "overtime":
                    sent_or_not = True
                send_msgs_info[phone_number].append({
                    "time": send_time,
                    "body": msg,
                    "sent": sent_or_not,
                })

            if len(send_msgs_info[phone_number]) == 0:
                del send_msgs_info[phone_number]
        return send_msgs_info

    def reset_sent_status(self):
        for phone_number in self.send_msgs_dict:
            for send_msg in phone_number:
                send_msg["sent"] = False


def check_timer_status(send_time):
    """Check if sending timer on schedule is on time or not

    Args:
        send_time (_string_): the sending timer on schedule

    Returns:
        _string_: determine the sending timer is ontime or not
            - If ontime: return "ontime"
            - Else if the time is over than 5 mins: return "overtime"
            - Else: return None
    """
    def get_mins(string_time):
        """Return total min from HH:MM time

        Args:
            string_time (_string_): the time with format HH:MM

        Returns:
            _int_: total min = hour*60 + min
        """
        h, m = string_time.split(":")
        return int(h)*60 + int(m)
    current_dtime = datetime.now()
    current_time = get_mins(current_dtime.strftime("%H:%M"))

    send_time = get_mins(str(send_time))

    if current_time > send_time + 5:
        return "overtime"
    elif current_time == send_time:
        return "ontime"
    return None
