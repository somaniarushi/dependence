import matplotlib.pyplot as plt
import networkx as nx

from lexer import Lexer
from parsers import Parser
from interpreter import Interpreter

def getEdges(text):
    lexer = Lexer(text)

    return [(1, 2), (1, 6), (2, 3), (2, 4),
         (2, 6), (3, 4), (3, 5), (4, 8),
         (4, 9), (6, 7)]


def main():
    import sys
    # text = open(sys.argv[1], 'r').read()
    text = open('inputs/input1.txt', 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    result = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)

    # edges = getEdges(text)

    # G = nx.Graph()
    # G.add_edges_from(edges)
    # nx.draw_networkx(G, with_labels = True)
    # plt.show()

if __name__ == '__main__':
    main()
