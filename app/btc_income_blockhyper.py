import json

from typing import List
from pydantic import BaseModel
from pathlib import Path
from blockcypher import get_address_full

from app.logger import logging
from app.config import BTC_WALLET, CONFIRMATIONS, BLOCK_HYPER_TOKEN


class Output(BaseModel):
    value: int
    addresses: List[str]


class Transaction(BaseModel):
    hash: str = None
    double_spend: bool = False
    confirmations: int = 0
    block_index: int = -1
    outputs: List[Output]

    @property
    def result(self):
        for output in self.outputs:
            if output.addresses == [BTC_WALLET]:
                return output.value


class WalletHistory(BaseModel):
    address: str
    n_tx: int
    final_balance: int
    txs: List[Transaction]


class BtcTransactions:
    CACHE_DIR = "cache"
    CACHE = f"{CACHE_DIR}/prev_bh_transactions.json"

    def __init__(self, wallet):
        self.wallet = wallet
        self.prev_wallet_history = None
        self.current_wallet_history = None
        self.new_transactions = None

    def _read_prev_transactions(self):
        try:
            with open(self.CACHE, "r") as openfile:
                return json.load(openfile)
        except FileNotFoundError:
            return

    def _write_prev_transactions(self, prev_transactions):
        Path(self.CACHE_DIR).mkdir(parents=True, exist_ok=True)

        try:
            with open(self.CACHE, "w") as f:
                json.dump(prev_transactions, f, default=str)
        except FileNotFoundError:
            return

    @staticmethod
    def _get_new_transactions(prev_wallet_history, current_wallet_history):
        prev_txs = set()
        new_transactions = []

        for tx in prev_wallet_history.txs:
            if tx.block_index > 0 and tx.confirmations > CONFIRMATIONS:
                prev_txs.add(tx.hash)

        for tx in current_wallet_history.txs:
            if (
                tx.block_index > 0
                and tx.confirmations > CONFIRMATIONS
                and tx.hash not in prev_txs
            ):
                new_transactions.append(tx)
                logging.info(tx)

        return new_transactions

    def get_new_transactions(self):
        logging.info("Fetch new data")
        result = get_address_full(address=BTC_WALLET, api_key=BLOCK_HYPER_TOKEN)

        self.current_wallet_history = WalletHistory.model_validate(result)

        prev_transactions = self._read_prev_transactions()
        self._write_prev_transactions(result)

        if not prev_transactions:
            return

        self.prev_wallet_history = WalletHistory.model_validate(prev_transactions)

        new_transactions = self._get_new_transactions(
            self.prev_wallet_history, self.current_wallet_history
        )

        return new_transactions
