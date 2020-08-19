from typing import Sequence
import numpy as np
from collections import defaultdict
from Exercises.tsp_lkh.bailian.jianshuzhi import Node


def create_init_tree(pickup_node: Node, deliver_nodes: Sequence[Node], td_matrix):
    nodes = [pickup_node]
    nodes.extend(deliver_nodes)
    dist = defaultdict(float)
    dist[0] = 0
    for i in range(len(deliver_nodes)):
        dist[i+1] = np.inf
    rest = dist.copy()
    while rest:
        adding_node_idx = min(rest, key=lambda x: rest[x])
        adding_node = nodes[adding_node_idx]
        if adding_node.parent is not None:
            adding_node.parent.children.append(adding_node)
        del rest[adding_node_idx]
        for v in rest.keys():
            if dist[v] > dist[adding_node_idx] + td_matrix[adding_node.name][nodes[v].name]:
                dist[v] = dist[adding_node_idx] + td_matrix[adding_node.name][nodes[v].name]
                nodes[v].parent = adding_node
                rest[v] = dist[v]
    return nodes
