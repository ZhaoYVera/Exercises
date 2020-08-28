import numpy as np


class Node:
    def __init__(self, name, volume=0, weight=0, time_window=None, lng=None, lat=None, district=None, branch_nodes=None):
        self.name = name
        self.volume = volume
        self.weight = weight
        self.time_window = time_window
        self.layer = 0
        self.parent = None
        self.children = []
        self.lng = lng
        self.lat = lat
        self.district = district
        self.key = np.inf  # used in Prim's algorithm
        self.branch_nodes = branch_nodes

    def __repr__(self):
        return self.name
