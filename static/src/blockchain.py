import hashlib
from time import time

from static.src.block import Block
import requests


class Blockchain(object):
    def __init__(self):
        self.blockchain = []
        self.current_transactions = []
        self.nodes = set()
        self.init_genesis()

    def init_genesis(self):
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        # print(address)
        # parsed_url = urlparse(address)
        # print(parsed_url.netloc)
        self.nodes.add(address)

    def validate(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            if block['previous_hash'] != Block.generate_hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        max_length = len(self.blockchain)

        for node in neighbours:
            print(f'http://{node}/chain')
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.validate(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.blockchain = new_chain
            return True
        return False

    @property
    def last_block(self):
        return self.blockchain[-1]

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
