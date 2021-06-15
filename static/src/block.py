import hashlib
import json



class Block:
    def __init__(self, transactions):
        self.transactions = transactions

    @staticmethod
    def generate_hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
