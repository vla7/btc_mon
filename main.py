import gc
import signal
import time

import app.config
from app import config
from app.btc_price import get_btc_price
from app.logger import logging
from app.tg_sender import send_transactions_to_tg

if app.config.HANDLER == "blockhyper":
    from app.btc_income_blockhyper import BtcTransactions
elif app.config.HANDLER == "blockchain":
    from app.btc_income_blockchain_info import BtcTransactions


def check_transactions():
    new_transactions = BtcTransactions(config.BTC_WALLET).get_new_transactions()

    if not new_transactions:
        return
    logging.info(new_transactions)

    btc_price = get_btc_price()

    send_transactions_to_tg(new_transactions, btc_price)


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
