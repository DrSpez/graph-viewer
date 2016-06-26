from pyexcel_xlsx import get_data
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
import json
import os
import pdb


def read_excel_graph(filename, draw=False):
    data = get_data(filename)
    G = nx.DiGraph()
    nodes = set([])
    edges = []

    i = 0
    for line in data.values():
        for v in line:
            i += 1
            if i > 2:
                node_id, void, a, b = v
                nodes.add(node_id)
                edges.append([a, b])

    try:
        nodes.remove(None)
    except:
        pass

    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    if draw:
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_color='yellow')
        nx.draw_networkx_edges(G, pos, edge_color='black')
        nx.draw_networkx_labels(G, pos, font_size=7)
        plt.show(block=False)

    return G

def write_graph_to_json(graph, save_to):
    Nodes = [{"name": n, "group": 0} for n in graph.nodes()]
    Index = {n["name"]: i for i, n in enumerate(Nodes)}
    Links = [{"source": Index[l[0]], "target": Index[l[1]], "value": 1}
             for l in graph.edges()]

    result = {"nodes": Nodes,
              "links": Links}
    with open(save_to, 'w') as outfile:
        json.dump(result, outfile)
