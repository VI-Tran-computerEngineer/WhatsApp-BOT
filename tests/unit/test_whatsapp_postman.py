import pytest

import whatsapp_postman as WhatApp
from datetime import datetime
import tests.unit.mock_data.mock_whatsapp_postman as mock_dat


def test_new_day(mocker):
    mocker.patch(
        "whatsapp_interaction.WhatsApp_API.__init__",
        return_value=None,
    )
    mocker.patch(
        "sql_connection.MySQL_connector.__init__",
        return_value=None,
    )
    mocker.patch(
        "whatsapp_postman.WhatsApp_user_callback.construct_data",
        return_value=[
            mock_dat.SEND_MSGS_DICT_NEW_DAY,
            mock_dat.RECV_STATS_NEW_DAY
        ],
    )

    whatsapp_class = WhatApp.WhatsApp_user_callback()
    whatsapp_class.reset_sent_status()
    assert whatsapp_class.send_msgs_dict == mock_dat.EXPECTED_SEND_MSGS_DICT_NEW_DAY
    assert whatsapp_class.recv_stats == mock_dat.EXPECTED_RECV_STATS_NEW_DAY


def test_feedback_msg_sent(mocker):
    mocker.patch(
        "whatsapp_interaction.WhatsApp_API.__init__",
        return_value=None,
    )
    mocker.patch(
        "sql_connection.MySQL_connector.__init__",
        return_value=None,
    )
    mocker.patch(
        "whatsapp_postman.WhatsApp_user_callback.construct_data",
        return_value=[
            mock_dat.SEND_MSGS_DICT_FEEDBACK_CASE,
            mock_dat.RECV_STATS_FEEDBACK_CASE,
        ],
    )
    mocker.patch(
        "sql_connection.MySQL_connector.query_user_info",
        return_value=mock_dat.RAW_USER_INFO,
    )

    whatsapp_class = WhatApp.WhatsApp_user_callback()
    whatsapp_class.send_feedback_msg()
