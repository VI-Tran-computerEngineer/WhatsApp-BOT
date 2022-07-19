"""Mock data for testing new day case."""
SEND_MSGS_DICT_NEW_DAY = {
    "0123456789": [
        {
            "time": "11:11",
            "body": "msg_a",
            "language": "en",
            "sent": True,
        },
        {
            "time": "12:11",
            "body": "msg_b",
            "language": "en",
            "sent": True,
        },
        {
            "time": "13:11",
            "body": "msg_c",
            "language": "en",
            "sent": True,
        }
    ],
    "9876543210": [
        {
            "time": "01:11",
            "body": "msg_a",
            "language": "en",
            "sent": False,
        },
        {
            "time": "02:11",
            "body": "msg_b",
            "language": "en",
            "sent": False,
        },
        {
            "time": "03:11",
            "body": "msg_c",
            "language": "en",
            "sent": True,
        }
    ]
}
EXPECTED_SEND_MSGS_DICT_NEW_DAY = {
    "0123456789": [
        {
            "time": "11:11",
            "body": "msg_a",
            "language": "en",
            "sent": False,
        },
        {
            "time": "12:11",
            "body": "msg_b",
            "language": "en",
            "sent": False,
        },
        {
            "time": "13:11",
            "body": "msg_c",
            "language": "en",
            "sent": False,
        }
    ],
    "9876543210": [
        {
            "time": "01:11",
            "body": "msg_a",
            "language": "en",
            "sent": False,
        },
        {
            "time": "02:11",
            "body": "msg_b",
            "language": "en",
            "sent": False,
        },
        {
            "time": "03:11",
            "body": "msg_c",
            "language": "en",
            "sent": False,
        }
    ]
}

RECV_STATS_NEW_DAY = {
    "0123456789": False,
    "9876543210": True
}
EXPECTED_RECV_STATS_NEW_DAY = {
    "0123456789": True,
    "9876543210": True
}
# **************************************************
"""Mock data for testing feedback msg case."""
SEND_MSGS_DICT_FEEDBACK_CASE = {
    "84342863321": [
        {
            "time": "13:11",
            "body": "msg_c",
            "language": "en",
            "sent": True,
        }
    ]
}
RECV_STATS_FEEDBACK_CASE = {
    "84342863321": True,
}
FEEDBACK_USER_INFO_FEEDBACK_CASE = {
    "84342863321": [
        {
            "option": "Option 2",
            "body": "testing",
        },
        {
            "option": "Option 2",
            "body": "testing_2",
        }
    ],
}

RAW_USER_INFO = [
    "LE VAN A",
    "25",
    "Vietnam",
]
EXPECTED_FEEDBACK_MSG = "Option 1: testing, Option 2: testing_2. This is just used for testing!"
# **************************************************
