"""This file contains all the necessary functions the orientations of at least digirth `k` of a graph."""

from time import process_time_ns

VISITED = 1
OUTGOING_ASSIGNMENT = "1"  # assignment coming from the vertex to be added
INCOMING_ASSIGNMENT = "0"  # assignment going to the vertex to be added


def time_digirthK_orientations(graph, digirth=Infinity):
    initial_t = process_time_ns()
    orientations = digirthK_orientations(graph, digirth)
    final_t = process_time_ns()
    print(
        f"Found {len(orientations)} orientations of at least digirth {digirth} in {(final_t-initial_t)/1000000000}s"
    )


def digirthK_orientations(graph, digirth=Infinity):
    """Public function to obtain the orientations with at least digirth `digirth` of a graph.
    If digirth is smaller than 3, it defaults to 3. If no digirth is provided,
    it defaults to infinity.Returns an EdgeView's list.
    """
    if digirth < 3:
        digirth = 3
    orientations = []
    digraph = DiGraph()
    _digirthK_orientations(graph, orientations, 0, digraph, digirth)
    return orientations


def _digirthK_orientations(graph, orientations, new_v_ind, digraph, digirth):
    """Recursive function to enumerate the orientations of a graph with at least digirth `digirth`."""
    if new_v_ind == graph.order():
        orientations.append(digraph.edges(labels=False))
        return
    neighbors = list(set(graph.neighbors(new_v_ind)).intersection(digraph.vertices()))
    if not neighbors:
        new_digraph = digraph.copy()
        new_digraph.add_vertex(new_v_ind)
        _digirthK_orientations(graph, orientations, new_v_ind + 1, new_digraph, digirth)
    else:
        legal_assignments(digraph, neighbors, digirth, graph, orientations, new_v_ind)


def legal_assignments(digraph, neighbors, digirth, graph, orientations, new_v_ind):
    """Auxiliar function to compute the legal assignments of a digraph given a new vertex."""
    initial_partial_assignment = INCOMING_ASSIGNMENT * len(neighbors)
    _legal_assignments(
        digraph,
        neighbors,
        initial_partial_assignment,
        0,
        digirth,
        graph,
        orientations,
        new_v_ind,
    )


def _legal_assignments(
    digraph,
    neighbors,
    partial_assignment,
    partial_assignment_ind,
    digirth,
    graph,
    orientations,
    new_v_id,
):
    """Recursive function to obtain the digraphs extended by all possible legal assignments"""
    legal_assignment = closure(digraph, partial_assignment, neighbors, digirth)
    if partial_assignment_ind == len(neighbors) and partial_assignment == legal_assignment:
        extended_digraph = extend(digraph, neighbors, partial_assignment, new_v_id)
        _digirthK_orientations(graph, orientations, new_v_id + 1, extended_digraph, digirth)
        return
    if partial_assignment[:partial_assignment_ind] == legal_assignment[:partial_assignment_ind]:
        _legal_assignments(
            digraph,
            neighbors,
            partial_assignment,
            partial_assignment_ind + 1,
            digirth,
            graph,
            orientations,
            new_v_id,
        )
    partial_assignment = (partial_assignment[:partial_assignment_ind] + "1" + partial_assignment[partial_assignment_ind + 1 :])
    legal_assignment = closure(digraph, partial_assignment, neighbors, digirth)
    if partial_assignment[:partial_assignment_ind] == legal_assignment[:partial_assignment_ind]:
        _legal_assignments(
            digraph,
            neighbors,
            partial_assignment,
            partial_assignment_ind + 1,
            digirth,
            graph,
            orientations,
            new_v_id,
        )


def extend(digraph, w, d, v):
    """Extends a digraph for the assignment d. Returns a new digraph."""
    new_digraph = digraph.copy()
    for ind, _ in enumerate(w):
        if d[ind] == INCOMING_ASSIGNMENT:
            new_digraph.add_edge(w[ind], v)
        else:
            new_digraph.add_edge(v, w[ind])
    return new_digraph


def closure(digraph, newD, w, digirth):
    """Computes the closure of assignment d of a digraph taking into accout the digirth."""
    tmpDigraph = digraph.copy()
    assignments = dict(zip(w, newD))
    v_out_assignments = [node for node, direciton in assignments.items() if direciton == OUTGOING_ASSIGNMENT]
    for vertex in v_out_assignments:
        _visit(vertex, tmpDigraph, assignments, digirth - 3)
    return "".join(assignments.values())


def _visit(vertex, digraph, assignment, counter):
    if counter == 0:
        return
    if digraph.get_vertex(vertex) == VISITED:
        return
    if vertex in assignment:
        assignment[vertex] = OUTGOING_ASSIGNMENT
    digraph.set_vertex(vertex, VISITED)
    for vertex2 in digraph.neighbors_out(vertex):
        _visit(vertex2, digraph, assignment, counter - 1)