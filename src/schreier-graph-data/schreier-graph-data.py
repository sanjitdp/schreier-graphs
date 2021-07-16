from itertools import product
from copy import deepcopy
import networkx as nx
from networkx import networkx
import graphviz
import os
import math

# constants that determine the graph that will be drawn

CYCLES = [6, 4]
PERMUTATION_CYCLES = [list(range(0, CYCLES[0])),
                      [0] + list(range(CYCLES[0], CYCLES[0] + CYCLES[1] - 1))]  # what are the permutation cycles?
DIRECTED = False  # are we studying the directed graph?
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
def odometer(cycle, v):
    if not v:
        return ()
    if v[0] in cycle:
        target = deepcopy(v)
        if v[0] == cycle[-1]:
            return cycle[0], *odometer(cycle, v[1:])
        else:
            target[0] = cycle[cycle.index(v[0]) + 1]
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
    for node in nodes:
        vertices.append(list(node))

    # edges will be a list of dictionaries from vertices to vertices,
    # where each cycle has its own list
    edges = []
    for index, cycle in enumerate(PERMUTATION_CYCLES):
        cycle_edges = {}
        for v in vertices:
            cycle_edges[tuple(v)] = tuple(odometer(cycle, v))
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
    c = [len(CYCLE) for CYCLE in PERMUTATION_CYCLES]
    a = c[0]
    b = c[1]
    print(TASK + ":", c)
    print("Micah's guess (level 2): ",
          math.floor(a / 2) * (2 * a + 1 - 2 * math.floor(a / 2)) + math.floor(b / 2) * (
                      a + b + 1 - 2 * math.floor((a + 1) / 2)))
    print("Gabriel's guess (level 2): ",
          (a % 2) * (math.floor(a / 2) * (a + 2) + b * math.floor(b / 2)) + ((a + 1) % 2) * (
                  math.floor(a / 2) * (a + 1) + math.floor(b / 2) * (b + 1)))

    if TASK == "VISUALIZE":
        do_task(LEVEL)
        exit(0)

    for n in range(1, LEVEL + 1):
        do_task(n)
        if a % 2 == 1 and b % 2 == 0:
            print("John's guess: ", (a ** n + a ** (n - 1) + b ** n - 2) / 2)
        if a % 2 == 1 and b % 2 == 1:
            print("John's guess: ", (a ** n + a ** (n - 1) + b ** n - b ** (n - 1) - 2) / 2)
        if a % 2 == 0 and b % 2 == 1:
            print("John's guess: ", (b ** n - 1 + a * (a ** n - 1) / (a - 1)) / 2)
        if a % 2 == 0 and b % 2 == 0:
            print("John's guess: ", a * (a ** n - 1) / (2 * (a - 1)) + b * (b ** n - 1) / (2 * (b - 1)))
