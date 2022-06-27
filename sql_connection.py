import mysql.connector
import configparser
from datetime import datetime
from exceptions import SQLConnectionError, SQLQueryError
# Get values from .ini file
config = configparser.ConfigParser()
config.read('config.ini')

HOST_NAME = config["mysql"]["hostname"]
USERNAME = config["mysql"]["username"]
PASSWORD = config["mysql"]["password"]
DATABASE_NAME = config["mysql"]["database_name"]

TO_PHONE_TABLE = config["mysql"]["to_phone_table"]
REPLIED_MSGS_TABLE = config["mysql"]["replied_msg_table"]


def connect_to_mysql():
    try:
        conn_object = mysql.connector.connect(
            host=HOST_NAME, user=USERNAME, password=PASSWORD, database=DATABASE_NAME)
        print("Connected to SQL database!")
    except:
        raise SQLConnectionError("Can't connect to MySQL database.")
    return conn_object


class MySQL_connector:
    def __init__(self):
        self.conn_object = connect_to_mysql()
        self.cursor = self.conn_object.cursor()

    def query_to_phone_number(self):
        query_cmd = f"SELECT phone_number, msg_sent_schedule FROM {TO_PHONE_TABLE}"
        try:
            self.cursor.execute(query_cmd)
        except BaseException as e:
            raise SQLQueryError(
                "Failed to query phone numbers from database!\n", e)
        table = self.cursor.fetchall()
        return table

    def query_msgs_schedule(self, schedule_name):
        query_cmd = f"SELECT sending_time, msg_name FROM {schedule_name}"
        try:
            self.cursor.execute(query_cmd)
        except BaseException as e:
            raise SQLQueryError(
                "Failed to query messages schedules from database!\n", e)
        table = self.cursor.fetchall()
        return table

    def store_reply_to_table(self, phone_number, sent_msg_info, reply_msg):
        current_day = datetime.now().strftime("%d:%m:%Y")
        sent_dtime = current_day + " " + sent_msg_info["time"]
        sent_msg = sent_msg_info["body"]
        query = f"INSERT INTO {REPLIED_MSGS_TABLE} (datetime, phone_number, sent_msg, replied_msg)"
        value = "VALUES (%s, %s, %s, %s)"
        query_cmd = query + value
        val = (sent_dtime, phone_number, sent_msg, reply_msg)
        try:
            self.cursor.execute(query_cmd, val)
            self.conn_object.commit()
        except BaseException as e:
            raise SQLQueryError(
                "Failed to save replied messages into database!\n", e)

    def query_reply_messages(self, phone_number):
        query_cmd = f"SELECT * FROM reply_messages WHERE phone_number=\"{phone_number}\""
        try:
            self.cursor.execute(query_cmd)
        except:
            raise SQLQueryError(
                "Failed to query messages schedules from database!")
        table = self.cursor.fetchall()
        return table
