""" 
With the Sage environment, this file contains a functions to compute the orientations
with at least digirth $k$ of a graph. It uses an approach similar to the Gray 
Algorithm.
"""

from time import process_time_ns


def time_gray_orientations(graph, digirth=+Infinity):
    """Helper function to time the gray algorithm."""
    initial_t = process_time_ns()
    orientations = gray_orientations(graph, digirth)
    final_t = process_time_ns()
    print(
        f"Found {len(orientations)} orientations of at least digirth {digirth} in {(final_t-initial_t)/1000000000}s"
    )

def gray_orientations(graph, digirth=+Infinity):
    """Computes the orientations of graph with at least digirth digirth using the gray's
    algorithm. If digirth is smaller than 3, it defaults to 3. If no digirth is provided,
    it defaults to infinity.Returns an EdgeView's list."""
    if digirth < 3:
        digirth = 3
    d_digirth_orientations = []
    for orientation in graph.orientations():
        if orientation.girth() >= digirth:
            d_digirth_orientations.append(orientation.edges(labels=False))
    return d_digirth_orientations
