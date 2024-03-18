from urllib.parse import quote
from datetime import datetime
import requests
import socket
import json
import os


def send_photo(file_path):
    token =  os.getenv('TELEGRAM_TOKEN')
    api_url = f'https://api.telegram.org/bot{token}/sendPhoto'
    hostname = socket.gethostbyname(os.getenv('HOSTNAME'))
    params = {'chat_id': os.getenv('TELEGRAM_CHATID'), 'caption': hostname }
    files = {'photo': open(file_path,'rb')}
    resp = requests.get(api_url, params, files=files)
    return resp


# Function send massage result to telegram chatbot
def send_message(text):
    token =  os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHATID')
    hostname = socket.gethostbyname(os.getenv('HOSTNAME'))
    encoded_text = quote(text)
    send_text = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={hostname} :\n{encoded_text}'
    try:
        resp = requests.get(send_text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    else:
        pass
    return resp

def send_error(e):
    token =  os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHATID')
    dt = datetime.now()
    json_e = json.dumps({'time': str(dt.time()).split('.')[0] + ' ' + str(dt.date()), 'Error': str(e)})
    hostname = socket.gethostbyname(os.getenv('HOSTNAME'))
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + hostname + ' :' + json_e
    resp = requests.get(send_text)
    return resp
