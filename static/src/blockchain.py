import hashlib
from time import time

import numpy as np

from static.src.block import Block


class Blockchain(object):
    def __init__(self):
        self.blockchain = []
        self.current_transactions = []
        self.init_genesis()

    def init_genesis(self):
        self.new_block(previous_hash=1, proof=100)

    def get_coordinates(self):
        pass

    @property
    def last_block(self):
        return self.blockchain[-1]

    def validate(self):
        pass

    def mine(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash):
        block = {
            'index': len(self.blockchain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or Block.generate_hash(self.last_block),
        }

        # Перезагрузка текущего списка транзакций
        self.current_transactions = []

        self.blockchain.append(block)
        return block

    def new_transaction(self, sender_id, route_length, coordinates):
        self.current_transactions.append({
            'sender_id': sender_id,
            'route_length': route_length,
            'coordinates': coordinates
        })

        return self.last_block['index'] + 1
