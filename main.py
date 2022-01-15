import matplotlib.pyplot as plt
import networkx as nx

from lexer import Lexer
from parsers import Parser
from interpreter import Interpreter

def getEdges(mappings):
    edges = []

    for key in mappings:
        values = mappings[key]
        for value in values:
            edges.append((key, value))

    return edges


def main():
    import sys
    # text = open(sys.argv[1], 'r').read()
    text = open('inputs/input1.txt', 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()

    edges = getEdges(interpreter.mapping)
    print(edges)

    G = nx.DiGraph()
    G.add_edges_from(edges)
    nx.draw_networkx(G, with_labels = True)
    plt.show()

if __name__ == '__main__':
    main()
