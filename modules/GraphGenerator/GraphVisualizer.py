import logging

import matplotlib.pyplot as plt
import networkx as nx
import scipy as sp


def graphVisualizer(connector):
    edges = getAllEdges(connector)

    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge['from'], edge['to'], weight=len(edge['transactionHashes']))
    pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
    nx.draw_networkx_nodes(G, pos, node_size=3)
    nx.draw_networkx_edges(G, pos)
    ax = plt.gca()
    ax.margins(0.03)
    plt.figure(dpi=2000)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    logging.info("The Graph adjency list is:")
    for line in nx.generate_adjlist(G):
        logging.info(line)


def getAllEdges(connector):
    return connector.getAllEdges()
