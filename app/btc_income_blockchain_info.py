import json
import requests

from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path


class Transaction(BaseModel):
    hash: str = None
    result: int = 0
    double_spend: bool = False
    block_index: Optional[int] = None


class WalletHistory(BaseModel):
    address: str
    n_tx: int
    final_balance: int
    txs: List[Transaction]


class BtcTransactions:
    URL = "https://blockchain.info/rawaddr/{BTC_WALLET}?confirmations=2"
    CACHE_DIR = "cache"
    CACHE = f"{CACHE_DIR}/prev_transactions.json"

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
                json.dump(prev_transactions, f)
        except FileNotFoundError:
            return

    @staticmethod
    def _fetch_transactions(prev_wallet_history, current_wallet_history):
        prev_txs = set()
        new_transactions = []

        for tx in prev_wallet_history.txs:
            if tx.block_index:
                prev_txs.add(tx.hash)

        for tx in current_wallet_history.txs:
            if tx.block_index and tx.hash not in prev_txs:
                new_transactions.append(tx)

        return new_transactions

    def get_new_transactions(self):
        url = self.URL.format(BTC_WALLET=self.wallet)
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Bad response code {response.status_code}")
            return

        result = response.json()
        self._write_prev_transactions(result)
        self.current_wallet_history = WalletHistory.model_validate(result)

        prev_transactions = self._read_prev_transactions()
        if not prev_transactions:
            return

        self.prev_wallet_history = WalletHistory.model_validate(prev_transactions)

        new_transactions = self._fetch_transactions(
            self.prev_wallet_history, self.current_wallet_history
        )

        return new_transactions
