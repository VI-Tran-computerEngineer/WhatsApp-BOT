import requests
from requests.structures import CaseInsensitiveDict
from json import dumps
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
cloud_version = config['whatsapp_api']['version']


def setup_header(token):
    headers = CaseInsensitiveDict()
    headers["Authorization"] = f"Bearer {token}"
    headers["Content-Type"] = "application/json"
    return headers


class WhatsApp_API:
    def __init__(self, phone_number_id, access_token, webhook_url):
        self.url = f"https://graph.facebook.com/{cloud_version}/{phone_number_id}/messages"
        self.headers = setup_header(access_token)
        self.webhook_url = webhook_url

    def send_message(self, to_phone_number, msg):
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone_number,
            "type": "template",
            "template": {
                "name": msg,
                "language": {
                    "code": "en_US"
                }
            }
        }
        try:
            resp = requests.post(
                self.url, headers=self.headers, data=dumps(data))
            resp.raise_for_status()
            if resp.status_code == 200:
                print(
                    f"Sent message to {to_phone_number} with context \"{msg}\"!")
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)

    def get_messages_received(self):
        webhook_msg_url = self.webhook_url + "/messages"
        try:
            resp = requests.get(url=webhook_msg_url)
            resp.raise_for_status()
            if resp.status_code == 200:
                return resp.json()
            return None
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
