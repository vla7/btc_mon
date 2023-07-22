import os

MAIN_LOOP_SLEEP_SECONDS = int(os.environ.get("MAIN_LOOP_SLEEP_SECONDS", "300"))
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
CONFIRMATIONS = int(os.environ.get("CONFIRMATIONS", "2"))
BTC_WALLET = os.environ.get("BTC_WALLET")
BLOCK_HYPER_TOKEN = os.environ.get("BLOCK_HYPER_TOKEN")
TG_TOKEN = os.environ.get("TG_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
HANDLER = os.environ.get("HANDLER", "blockchain")
