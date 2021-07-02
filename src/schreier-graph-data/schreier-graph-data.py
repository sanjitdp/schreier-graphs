from itertools import product
from copy import deepcopy
import networkx as nx

# import pygraphviz

# constants that determine the graph that will be drawn
NUMBER_OF_LETTERS = 3
PERMUTATION_CYCLES = [[0, 1], [0, 2]]


# given a cycle c (a list of tuples) and a word v (a tuple),
# return the odometer's action on v
def odometer(c, v):
    if not v:
        return ()
    if v[0] in c:
        target = deepcopy(v)
        if v[0] == c[-1]:
            return c[0], *odometer(c, v[1:])
        else:
            target[0] = c[c.index(v[0]) + 1]
            return tuple(target)
    else:
        return tuple(v)


# returns a set of edges and vertices given a list of cycles, a word length,
# and number of letters in the alphabet
def make_graph(word_length):
    # letters are all numbers between 0 and NUMBER_OF_LETTERS
    letters = range(0, NUMBER_OF_LETTERS)

    # take Cartesian power to figure out what the nodes are
    nodes = list(product(letters, repeat=word_length))
    vertices = []
    for n in nodes:
        vertices.append(list(n))

    # edges will be a list of dictionaries from vertices to vertices,
    # where each cycle has its own list
    edges = []
    for i, c in enumerate(PERMUTATION_CYCLES):
        cycle_edges = {}
        for v in vertices:
            cycle_edges[tuple(v)] = tuple(odometer(c, v))
        edges.append(cycle_edges)

    return nodes, edges


if __name__ == "__main__":
    # find edges and vertices using above function
    for i in range(1, 6):
        graph = make_graph(i)

        # create a graph using networkx
        network = nx.MultiDiGraph()

        for node in graph[0]:
            network.add_node(node)

        for cycle in graph[1]:
            for edge in cycle:
                network.add_edge(edge, cycle[edge])

        print(nx.algorithms.distance_measures.diameter(network))

    # convert graph and plot it using pygraphviz
    # a = nx.nx_agraph.to_agraph(network)
    # a.layout(prog="neato")
    #
    # a.draw("graph.png")
