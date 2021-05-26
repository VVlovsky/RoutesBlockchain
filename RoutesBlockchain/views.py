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


def full_chain(*args):
    print(*args)
    response = {
        'chain': blockchain.blockchain,
        'length': len(blockchain.blockchain),
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


def mine(*args):
    print(args)
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


# @app.route('/nodes/register', methods=['POST'])
def register_nodes(request):
    # print("ans: ")
    # print(request.body)
    values = json.loads(request.body)
    print(values)
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return HttpResponse(status=201, content=json.dumps(response))


# @app.route('/nodes/resolve', methods=['GET'])
def consensus(*args):
    print(args)
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.blockchain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.blockchain
        }

    return HttpResponse(status=200, content=json.dumps(response))
