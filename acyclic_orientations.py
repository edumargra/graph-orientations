"""This file contains the necessary functions to compute the acyclic orientations of a graph.
The implementation is based on the algorithm by Barbosa and Szwarcfiter.
"""
from time import process_time_ns


def _closure(digraph, d, w):
    """Computes the closure of assignment d of a digraph."""
    incoming_edges = {}
    for vertex in digraph.vertices():
        incoming_edges[vertex] = len(digraph.neighbors_in(vertex))
    sources = set(digraph.sources())
    assignments = dict(zip(w, d))
    outgoing_in_d = {vertex for vertex, assignment in assignments.items() if assignment == "1"}
    while sources:
        source = sources.pop()
        neighbors_out = digraph.neighbors_out(source)
        for vertex in neighbors_out:
            incoming_edges[vertex] -= 1
            if source in outgoing_in_d:
                if vertex in assignments.keys():
                    assignments[vertex] = 1
                outgoing_in_d.add(vertex)
            if not incoming_edges[vertex]:
                sources.add(vertex)
    legal_d = "".join((str(value) for value in assignments.values()))
    return legal_d


def _next_legal_assignment(digraph, w, d):
    last_zero = d.rfind("0")
    next_d = f"{d[:last_zero]}1{'0'*(len(w)-(last_zero+1))}"
    return _closure(digraph, next_d, w)


def _extend(digraph, w, d, v):
    """Extends a digraph for the assignment d. Returns a new digraph."""
    newDigraph = digraph.copy()
    for ind, _ in enumerate(w):
        if d[ind] == "0":
            newDigraph.add_edge(w[ind], v)
        else:
            newDigraph.add_edge(v, w[ind])
    return newDigraph


def _acyclic_orientations(graph, index=0, digraph=DiGraph(), orientations=[]):
    """Recursive call to enumerate the acyclic orientations of a graph."""
    if index == (graph.order()):
        orientations.append(digraph.edges(labels=False))
        return
    neighbors = list(set(graph.neighbors(index)).intersection(digraph.vertices()))
    if neighbors == []:
        newDigraph = digraph.copy()
        newDigraph.add_vertex(index)
        _acyclic_orientations(graph, index + 1, newDigraph, orientations)
    else:
        w = [vertex for vertex in digraph.topological_sort() if vertex in neighbors]
        d = "0" * len(neighbors)
        last = False
        while not last:
            newDigraph = _extend(digraph, w, d, index)
            _acyclic_orientations(graph, index + 1, newDigraph, orientations)
            if d != "1" * len(neighbors):
                d = _next_legal_assignment(digraph, w, d)
            else:
                last = True

def acyclic_orientations(graph):
    """Public function to obtain the acyclic orientations of a graph. Based
    on the algorithm by Barbosa and Szwarcfiter. Raises an error if the correct
    number of orientations is not obtained. Returns a EdgeView's list otherwise."""
    orientations = []
    _acyclic_orientations(graph, orientations=orientations)
    if len(orientations) != graph.tutte_polynomial()(2, 0):
        raise ValueError("There is a problem with the algorithm and the graph.")
    return orientations


def time_acyclic_orientations(graph):
    initial_t = process_time_ns()
    orientations = acyclic_orientations(graph)
    final_t = process_time_ns()
    print(f"Found {len(orientations)} acyclic orientations in {(final_t-initial_t)/1000000000}s")
