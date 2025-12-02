import itertools


def exact_mis(graph):
    """
    Finds the largest independent set of a graph by iterating
    through all possible sub graphs, checking if the sub graph
    is larger than the current largest independent set. It then
    checks if the subset is an independent set, if it is, it becomes
    the new largest independent set.
    """
    largest_mis = {}
    for subset in all_subsets(graph):
        if len(subset) > len(largest_mis) and is_independent_set(subset):
            largest_mis = subset
    return largest_mis


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
    for r in range(len(keys) + 1):
        for combo in itertools.combinations(keys, r):
            yield {key: graph[key] for key in combo}

