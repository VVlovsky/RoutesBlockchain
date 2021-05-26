import numpy as np


class Transaction:
    def __init__(self, transaction_id, sender_id, route_length, coordinates):
        self.id = transaction_id
        self.sender_id = sender_id
        self.trajectory_length = route_length
        self.coordinates = coordinates

