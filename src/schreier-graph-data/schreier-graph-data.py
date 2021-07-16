from itertools import product
from copy import deepcopy
import networkx as nx
from networkx import networkx
import graphviz
import os

# constants that determine the graph that will be drawn

PERMUTATION_CYCLES = [[0, 1], [0, 2, 3]]  # what are the permutation cycles?
DIRECTED = True  # are we studying the directed graph?
TASK = "DIAMETER"  # what task are we doing?
LEVEL = 5  # level to which the program should be run
DIRNAME = "../../output/schreier-graph-visualization"  # directory in which to save the output file


# function to visualize graph

def visualize(nk):
    # change into the output directory
    try:
        os.mkdir(DIRNAME)
    except FileExistsError:
        pass
    finally:
        os.chdir(DIRNAME)

    # convert graph to DOT language format and save to file
    nx.drawing.nx_pydot.write_dot(nk, "graph")

    # render graph and remove unnecessary temporary DOT file
    graphviz.render('neato', 'png', "graph")
    os.remove("graph")

    return "Graph has been drawn successfully!"


# dictionary containing all possible tasks

TASKS_DICTIONARY = {
    "VISUALIZE": visualize,
    "RADIUS": lambda nk: networkx.algorithms.distance_measures.radius(nk),
    "DIAMETER": lambda nk: networkx.algorithms.distance_measures.diameter(nk),
    "PERIPHERY": lambda nk: networkx.algorithms.distance_measures.periphery(nk),
    "ECCENTRICITIES": lambda nk: networkx.algorithms.distance_measures.eccentricity(nk)
}


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
    # how many letters are in the alphabet we're working with?
    number_of_letters = max(CYCLE[-1] for CYCLE in PERMUTATION_CYCLES) + 1

    # letters are all numbers between 0 and NUMBER_OF_LETTERS
    letters = range(0, number_of_letters)

    # take Cartesian power to figure out what the nodes are
    nodes = list(product(letters, repeat=word_length))
    vertices = []
    for n in nodes:
        vertices.append(list(n))

    # edges will be a list of dictionaries from vertices to vertices,
    # where each cycle has its own list
    edges = []
    for index, c in enumerate(PERMUTATION_CYCLES):
        cycle_edges = {}
        for v in vertices:
            cycle_edges[tuple(v)] = tuple(odometer(c, v))
        edges.append(cycle_edges)

    # create a graph using networkx
    network = nx.MultiDiGraph() if DIRECTED else nx.MultiGraph()

    # find edges and vertices using above function
    for node in nodes:
        network.add_node(node)

    for cycle in edges:
        for edge in cycle:
            network.add_edge(edge, cycle[edge], name=str(cycle))

    return network


# do task depending on TASK constant defined above
def do_task(level):
    graph = make_graph(level)
    print(TASKS_DICTIONARY[TASK](graph))


if __name__ == "__main__":
    print(TASK + ":", PERMUTATION_CYCLES)

    if TASK == "VISUALIZE":
        do_task(LEVEL)
        exit(0)

    for i in range(1, LEVEL + 1):
        do_task(i)
