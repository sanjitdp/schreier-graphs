from itertools import product
from copy import deepcopy
import networkx as nx
import graphviz as gv
import numpy as np
import sympy as sym
import os

# constants that determine the graph that will be drawn
PERMUTATION_CYCLES = [[0, 1], [0, 2]]  # what are the permutation cycles?
DIRECTED = False  # are we studying the directed graph?
TASK = "ADJ_EIGENVECTORS"  # what task are we doing?
LEVEL = 2  # level to which the program should be run
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
    gv.render('neato', 'png', "graph")
    os.remove("graph")

    return "Graph has been drawn successfully!"


# returns a string containing the factored characteristic polynomial
def adj_char_poly(nk):
    adjacency_matrix = sym.Matrix(nx.to_numpy_matrix(nk))
    char_poly = adjacency_matrix.charpoly()
    cp = str(sym.Poly(char_poly, domain="ZZ"))
    to_factor = cp[5:].split(",")[0].replace("lambda", "x")
    return sym.polys.polytools.factor(to_factor)


# dictionary containing all possible tasks
TASKS_DICTIONARY = {
    "VISUALIZE": visualize,
    "RADIUS": lambda nk: nx.algorithms.distance_measures.radius(nk),
    "DIAMETER": lambda nk: nx.algorithms.distance_measures.diameter(nk),
    "PERIPHERY": lambda nk: nx.algorithms.distance_measures.periphery(nk),
    "ECCENTRICITIES": lambda nk: nx.algorithms.distance_measures.eccentricity(nk),
    "ADJACENCY_MATRIX": lambda nk: nx.linalg.graphmatrix.adjacency_matrix(nk).todense(),
    "ADJ_SPECTRUM": lambda nk: repr(nx.linalg.spectrum.adjacency_spectrum(nk)),
    "ADJ_CHAR_POLY": adj_char_poly,
    "ADJ_EIGENVECTORS": lambda nk: repr(np.linalg.eig(nx.to_numpy_matrix(nk))[1].transpose()),
    "LAP_SPECTRUM": lambda nk: repr(nx.linalg.spectrum.laplacian_spectrum(nk)),
    "NORM_LAP_SPECTRUM": lambda nk: repr(nx.linalg.spectrum.normalized_laplacian_spectrum(nk)),
    "HES_SPECTRUM": lambda nk: repr(nx.linalg.spectrum.bethe_hessian_spectrum(nk)),
    "MOD_SPECTRUM": lambda nk: repr(nx.linalg.spectrum.modularity_spectrum(nk))
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
    network = nx.MultiDiGraph()

    # find edges and vertices using above function
    for node in nodes:
        network.add_node(node)

    for cycle in edges:
        for edge in cycle:
            network.add_edge(edge, cycle[edge], name=str(cycle))

    if not DIRECTED:
        directed_matrix = nx.to_numpy_matrix(network)
        undirected_matrix = np.add(directed_matrix, directed_matrix.transpose())
        return nx.from_numpy_matrix(undirected_matrix, parallel_edges=True, create_using=nx.MultiGraph)

    return network


# do task depending on TASK constant defined above
def do_task(level):
    graph = make_graph(level)
    print("LEVEL:", level)
    print(TASKS_DICTIONARY[TASK](graph), "\n")


if __name__ == "__main__":
    print(TASK + ":", PERMUTATION_CYCLES, "\n")
    if TASK == "VISUALIZE":
        do_task(LEVEL)
        exit(0)

    for n in range(1, LEVEL + 1):
        do_task(n)
