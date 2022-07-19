import collections
import time
from datetime import datetime
import configparser
from math import floor

from whatsapp_interaction import WhatsApp_API
from sql_connection import MySQL_connector

# Get values from .ini file
config = configparser.ConfigParser()
config.read('config.ini')
WAITING_SENT_INTERVAL = int(config['system']['waiting_sent_interval'])
WAITING_RECV_INTERVAL = int(config['system']['waiting_received_interval'])
NO_REPLIED_MSG_NAME = config['system']['no_replied_msg_name']
SEND_FEEDBACK_TIME = config['system']['send_feedback_time']


class WhatsApp_user_callback:
    def __init__(self):
        """."""
        self.whatsapp_api = WhatsApp_API()
        self.sql_connector = MySQL_connector()
        self.send_msgs_dict, self.recv_stats = self.construct_data()
        self.feedback_msg_triggers = []

    def send_preschedule_msgs(self):
        """The progress finds and sends scheduled message to users.
        """
        def sort_list(data_list):
            data_list = collections.deque(data_list)
            data_list.rotate(-1)
            return list(data_list)

        def is_next_day(dtime):
            current_day = datetime.now().strftime("%d/%m/%Y")
            if current_day != dtime:
                return True
            return False

        if len(self.send_msgs_dict) == 0:
            print("No msg needs to send!")
            return

        to_phone_numbers = list(self.send_msgs_dict.keys())
        for phone_number in to_phone_numbers:
            while True:
                send_msgs = self.send_msgs_dict[phone_number]
                if self.check_phone_number_done(phone_number) or not send_msgs[0]["sent"]:
                    break
                self.send_msgs_dict[phone_number] = sort_list(send_msgs)

        send_msgs_done = self.done_the_bot_today()
        current_day = None

        while True:
            time.sleep(WAITING_SENT_INTERVAL)

            # Check if the new day is comming
            current_day = datetime.now().strftime("%d/%m/%Y")
            if is_next_day(current_day) and current_day != None:
                send_msgs_done = False
                self.reset_sent_status()
            if send_msgs_done:
                if check_timer_status(SEND_FEEDBACK_TIME) in ["ontime", "overtime"]:
                    self.send_feedback_msg()
                continue
            for phone_number in to_phone_numbers:
                send_msgs = self.send_msgs_dict[phone_number]
                if (
                    not self.recv_stats[phone_number]
                    and send_msgs[0]["body"] != NO_REPLIED_MSG_NAME
                ):
                    continue
                # if sent the msg before ==> ignore the phone number
                if send_msgs[0]["sent"]:
                    self.send_msgs_dict[phone_number] = sort_list(send_msgs)
                    continue
                send_time = send_msgs[0]["time"]
                msg = send_msgs[0]["body"]
                language = send_msgs[0]["language"]

                timer_status = check_timer_status(send_time)
                if timer_status in ["ontime", "overtime"]:
                    self.whatsapp_api.send_message(phone_number, msg, language)
                    send_msgs[0]["sent"] = True
                    if send_msgs[0]["body"] != NO_REPLIED_MSG_NAME:
                        self.recv_stats[phone_number] = False
                    self.send_msgs_dict[phone_number] = sort_list(send_msgs)

            send_msgs_done = self.done_the_bot_today()
            if send_msgs_done:
                print("All messages sent today!\nWaiting for tomorrow.......")

    def wait_4_msgs_received(self):
        """Waiting for user's replied message and save it into database.
        """
        while True:
            if self.is_any_phone_number_waiting():
                received_msgs = self.whatsapp_api.get_messages_received()
                if received_msgs:
                    for recv_msg in received_msgs["data"]:
                        from_phone_number = recv_msg["from"]
                        recved_msg = recv_msg["body"]
                        print(f"Received message from {from_phone_number}!")
                        send_msg_info = self.send_msgs_dict[from_phone_number][-1]
                        self.sql_connector.store_reply_to_table(
                            from_phone_number, send_msg_info, recved_msg)
                        self.recv_stats[from_phone_number] = True

                        if self.check_phone_number_done(from_phone_number):
                            self.feedback_msg_triggers.append(
                                from_phone_number)

                    received_msgs = None

            time.sleep(WAITING_RECV_INTERVAL)

    def send_feedback_msg(self):
        """Send feedback messages include user information in the scheduled time.
        """
        if len(self.feedback_msg_triggers) == 0:
            return
        for phone_number in self.feedback_msg_triggers:
            user_info = self.sql_connector.query_user_info(phone_number)
            if user_info:
                feedback_msg = ", ".join(map(str, user_info))
                self.whatsapp_api.send_custom_message(
                    phone_number, feedback_msg
                )
                self.feedback_msg_triggers.remove(phone_number)

    def is_any_phone_number_waiting(self):
        """Check if any the scheduled message is sent,
        but currently the user hasn't answered.

        Returns:
            _bool_: True if the scheduled message is waiting feedback.
        """
        phone_numbers = list(self.recv_stats.keys())
        for phone_number in phone_numbers:
            if not self.recv_stats[phone_number]:
                return True
        return False

    def done_the_bot_today(self):
        """Check if all scheduled messages is sent
        and the BOT received all replied messages from user.

        Returns:
            _bool_: True if the condition is true
        """
        phone_numbers = list(self.send_msgs_dict.keys())
        for phone_number in phone_numbers:
            if not self.send_msgs_dict[phone_number][0]["sent"]:
                return False
        return True

    def check_phone_number_done(self, phone_number):
        """Check if all of the scheduled messages for the phone number
        have been sent.

        Args:
            phone_number (_str_): user's phone number

        Returns:
            _bool_: True if all messages have been sent
        """
        for msg in self.send_msgs_dict[phone_number]:
            if msg["sent"] == False:
                return False
        return True

    def construct_data(self):
        """Construct queried data from database to dictionary variables.
        """
        def sort_key(e):
            return get_mins(e["time"])
        phone_number_list = self.sql_connector.query_to_phone_number()
        send_msgs_info = {}
        for phone_number, schedule_name in phone_number_list:
            send_msgs_info[phone_number] = []

            msgs_schedule = self.sql_connector.query_msgs_schedule(
                schedule_name)
            for send_time, msg, language in msgs_schedule:
                sent_or_not = False
                if check_timer_status(send_time) == "overtime":
                    sent_or_not = True
                send_msgs_info[phone_number].append({
                    "time": send_time,
                    "body": msg,
                    "language": language,
                    "sent": sent_or_not,
                })

            send_msgs_info[phone_number].sort(key=sort_key)

            if len(send_msgs_info[phone_number]) == 0:
                del send_msgs_info[phone_number]
        recv_stats = {}
        to_phone_numbers = list(send_msgs_info.keys())

        for phone_number in to_phone_numbers:
            recv_stats[phone_number] = True
        return send_msgs_info, recv_stats

    def reset_sent_status(self):
        """Reset all variables to default value.
        """
        to_phone_numbers = list(self.send_msgs_dict.keys())
        for phone_number in to_phone_numbers:
            self.recv_stats[phone_number] = True
            for i in range(len(self.send_msgs_dict[phone_number])):
                self.send_msgs_dict[phone_number][i]["sent"] = False
        self.feedback_msg_triggers[:] = []


def get_mins(string_time):
    """Return total min from HH:MM time

    Args:
        string_time (_string_): the time with format HH:MM

    Returns:
        _int_: total min = hour*60 + min
    """
    h, m = string_time.split(":")
    return int(h)*60 + int(m)


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
    current_dtime = datetime.now()
    current_time = get_mins(current_dtime.strftime("%H:%M"))

    send_time = get_mins(str(send_time))
    if current_time > send_time + 5:
        return "overtime"
    elif send_time + 5 >= current_time >= send_time:
        return "ontime"
    return None
