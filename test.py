import random
import requests
from time import sleep


def generate_transaction():
    result = {}
    sender_id = ''.join(str(random.choice(range(10))) for _ in range(16))
    result |= {"sender_id": sender_id}
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    route = []
    route_length = random.randint(10, 50)
    for _ in range(route_length):
        if random.randint(0, 100) > 50:
            x += random.choice([-1, 1])
        else:
            y += random.choice([-1, 1])
        route.append(f'{x}, {y}')
    result |= {"coordinates": sender_id}
    result |= {"route_length": sender_id}

    return result


nodes_clean = ['95.179.240.109', '192.248.191.151', '45.76.82.209', '209.250.233.1',
         '192.248.184.111', '192.248.190.185', '45.63.119.143', '80.240.16.250',
         '95.179.251.26', '192.248.177.110']
# nodes_clean = ['127.0.0.1', '127.0.0.2', '127.0.0.3']

nodes = list(map(lambda x: 'http://' + x, nodes_clean))

for node in nodes:
    r = requests.get(f'{node}:8000')
    print(r.status_code, r.reason)

for node in nodes:
    print(f'{node}:8000/nodes/register')
    print(str([node_inner + ':8000' for node_inner in nodes_clean if node[7:] != node_inner]).replace("'", '"'))
    r = requests.post(f'{node}:8000/nodes/register', json={
        "nodes": [node_inner + ':8000' for node_inner in nodes_clean if node[7:] != node_inner]
    })
    print(r.status_code, r.reason)

while True:
    node_id = random.randint(0, len(nodes)-1)
    print(f'Running resolve on node {nodes[node_id]}')
    r = requests.get(f'{nodes[node_id]}:8000/nodes/resolve')
    print(r.status_code, r.reason)
    for i in range(random.randint(1, 5)):
        print(f'Running new transaction on node {nodes[node_id]}')
        r = requests.post(f'{nodes[node_id]}:8000/transactions/new', json=generate_transaction())
        print(r.status_code, r.reason)

    print(f'Running mine on node {nodes[node_id]}')
    r = requests.get(f'{nodes[node_id]}:8000/mine')
    print(r.status_code, r.reason)
    sleep(2)