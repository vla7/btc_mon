import requests

from app.logger import logging
from app.config import TG_TOKEN, TG_CHAT_ID

get_updates_url = "https://api.telegram.org/bot{TOKEN}/getUpdates"
send_url = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=HTML"


def get_updates():
    logging.info(requests.get(get_updates_url.format(TOKEN=TG_TOKEN)).json())


def send_transactions_to_tg(new_transactions, btc_price):
    message = ""
    for transaction in new_transactions:
        message += "<b>New transaction:</b>\n"
        message += transaction.hash + "\n"
        btc_sum = transaction.result / 100000000
        message += str("{:.8f}".format(btc_sum)) + " BTC\n"
        message += str("{:.2f}".format(btc_sum * btc_price)) + " USD\n"
        if transaction.double_spend:
            message += "<b>DOUBLE SPEND!:</b>\n"
        message += "\n"
    message.strip("\n")

    url = send_url.format(TOKEN=TG_TOKEN, CHAT_ID=TG_CHAT_ID, message=message)
    requests.get(url).json()
