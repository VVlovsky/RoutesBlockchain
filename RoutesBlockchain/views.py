import json
from uuid import uuid4
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from static.src.block import Block
from static.src.blockchain import Blockchain

global node_identifier, blockchain


def index(request):
    global blockchain, node_identifier
    node_identifier = str(uuid4()).replace('-', '')
    blockchain = Blockchain()
    context = {}
    return render(request, 'main_page/index.html', context)


def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return HttpResponse(status=200, content=json.dumps(response))


def new_transaction(request):
    data = json.loads(request.body)
    required = ['sender_id', 'coordinates', 'route_length']
    if not all(k in data for k in required):
        return HttpResponse(status=401, content=json.dumps({'message': "Missing Values"}))

    transaction_id = blockchain.new_transaction(data['sender_id'], data['coordinates'], data['route_length'])
    response = {'message': f'Transaction will be added to Block {transaction_id}'}
    return HttpResponse(status=201, content=json.dumps(response))


def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.mine(last_proof)

    previous_hash = Block.generate_hash(blockchain.last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return HttpResponse(status=200, content=json.dumps(response))
