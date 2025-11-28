import time
import json
from crypto import Wallet

class Transaction:
    def __init__(self, sender_pubkey, receiver_pubkey, amount, action="transfer", data=None, signature=None):
        self.sender = sender_pubkey
        self.receiver = receiver_pubkey
        self.amount = amount
        self.action = action # transfer, deposit, borrow, repay
        self.data = data # Extra data if needed
        self.timestamp = time.time()
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "action": self.action,
            "data": self.data,
            "timestamp": self.timestamp
        }

    def get_hashable_string(self):
        # Create a string representation for signing (excluding signature)
        # Ensure deterministic order
        data = self.to_dict()
        return json.dumps(data, sort_keys=True)

    def sign(self, wallet):
        message = self.get_hashable_string()
        self.signature = wallet.sign(message)

    def is_valid(self):
        if not self.signature:
            return False
        message = self.get_hashable_string()
        return Wallet.verify(message, self.signature, self.sender)

class Ledger:
    def __init__(self):
        self.chain = [] # List of blocks or just transactions for simplicity
        self.state = {} # Map address -> balance (or other state)
        # For this simulation, we'll keep a simple state mapping
        # address -> { "ETH": 100, "USDC": 500 }

    def get_balance(self, address, token="ETH"):
        user_state = self.state.get(address, {})
        return user_state.get(token, 0.0)

    def update_balance(self, address, amount, token="ETH"):
        if address not in self.state:
            self.state[address] = {}
        current = self.state[address].get(token, 0.0)
        self.state[address][token] = current + amount

    def process_transaction(self, tx):
        if not tx.is_valid():
            raise ValueError("Invalid signature")
        
        # Basic transfer logic
        if tx.action == "transfer":
            sender_bal = self.get_balance(tx.sender)
            if sender_bal < tx.amount:
                raise ValueError("Insufficient funds")
            
            self.update_balance(tx.sender, -tx.amount)
            self.update_balance(tx.receiver, tx.amount)
            
        self.chain.append(tx)
        return True
