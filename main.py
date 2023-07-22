import gc
import signal
import time

import requests

import app.config
from app import config
from app.btc_price import get_btc_price
from app.config import TG_TOKEN, TG_CHAT_ID
from app.logger import logging

if app.config.HANDLER == "blockhyper":
    from app.btc_income_blockhyper import BtcTransactions
elif app.config.HANDLER == "blockchain":
    from app.btc_income_blockchain_info import BtcTransactions


get_updates_url = "https://api.telegram.org/bot{TOKEN}/getUpdates"
send_url = "https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}&parse_mode=HTML"


def get_updates():
    print(requests.get(get_updates_url.format(TOKEN=TG_TOKEN)).json())


def send_message(message):
    url = send_url.format(TOKEN=TG_TOKEN, CHAT_ID=TG_CHAT_ID, message=message)
    requests.get(url).json()


def check_transactions():
    new_transactions = BtcTransactions(config.BTC_WALLET).get_new_transactions()

    if not new_transactions:
        return

    btc_price = get_btc_price()

    message = ""
    for transaction in new_transactions:
        message += "<b>New transaction:</b>\n"
        message += transaction.hash + "\n"
        message += str("{:.8f}".format(transaction.result / 100000000)) + " BTC\n"
        message += (
            str("{:.2f}".format(transaction.result / 100000000 * btc_price)) + " USD\n"
        )
        if transaction.double_spend:
            message += "<b>DOUBLE SPEND!:</b>\n"
        message += "\n"
    message.strip("\n")

    send_message(message)
    logging.info(message)


run = True


def handler_stop_signals(*_):
    global run
    run = False


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)
# signal.signal(signal.SIGHUP, handler_hup)

logging.info("BTC mon started")
while run:
    check_transactions()
    gc.collect()  # garbage collect
    for i in range(config.MAIN_LOOP_SLEEP_SECONDS):
        if run:
            time.sleep(1)
else:
    logging.info("SIGINT or SIGTERM received. Terminating")
