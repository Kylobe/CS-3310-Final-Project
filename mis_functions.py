import itertools
import random

def exact_mis(graph):
    """
    Finds the largest independent set of a graph by iterating
    through all possible sub graphs, checking if the sub graph
    is larger than the current largest independent set. It then
    checks if the subset is an independent set, if it is, it becomes
    the new largest independent set.
    """
    for subset in all_subsets(graph):
        if is_independent_set(subset):
            return subset


def is_independent_set(subset):
    """
    Checks if the inputted subset is an independent set
    and returns a bool.
    """
    for node in subset:
        for neighbor in subset[node]:
            if neighbor in subset:
                return False
    return True

def all_subsets(graph):
    """
    Defines a generator that enumerates all possible sub graphs
    of a given graph. It assumes the input graph is a dictionary 
    where each key is a vertex and maps to its adjacency list. The
    returned sub graph also follows the same architecture.
    """
    keys = list(graph.keys())
    for r in range(len(keys), 0, -1):
        for combo in itertools.combinations(keys, r):
            yield {key: graph[key] for key in combo}

def random_mis(graph: dict):
    # graph: dict[node, list_of_neighbors]
    remaining = set(graph.keys())
    mis_nodes = set()

    while remaining:

        chosen_node = random.choice(tuple(remaining))

        # add to MIS
        mis_nodes.add(chosen_node)

        # remove it and its neighbors from remaining
        remaining.remove(chosen_node)
        for neighbor in graph[chosen_node]:
            remaining.discard(neighbor)

    # if you really want the MIS as a "subgraph dict"
    return {node: graph[node] for node in mis_nodes}


def greedy_mis(graph: dict):
    # graph: dict[node, list_of_neighbors]
    remaining = set(graph.keys())
    mis_nodes = set()

    while remaining:
        # choose node with minimum degree *within remaining*
        def degree_in_remaining(u):
            return sum(1 for v in graph[u] if v in remaining)

        least_node = min(remaining, key=degree_in_remaining)

        # add to MIS
        mis_nodes.add(least_node)

        # remove it and its neighbors from remaining
        remaining.remove(least_node)
        for neighbor in graph[least_node]:
            remaining.discard(neighbor)

    # if you really want the MIS as a "subgraph dict"
    return {node: graph[node] for node in mis_nodes}


