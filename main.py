import matplotlib.pyplot as plt
import networkx as nx

def getEdges(text):
    return [(1, 2), (1, 6), (2, 3), (2, 4),
         (2, 6), (3, 4), (3, 5), (4, 8),
         (4, 9), (6, 7)]


def main():
    import sys
    text = open(sys.argv[1], 'r').read()

    edges = getEdges(text)

    G = nx.Graph()
    G.add_edges_from(edges)
    nx.draw_networkx(G, with_labels = True)
    plt.show()