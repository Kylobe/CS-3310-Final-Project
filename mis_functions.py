import itertools
import random
from typing import Mapping, Iterable, Dict
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

def random_improve(graph: Mapping[str, Iterable[str]]) -> Dict[str, Iterable[str]]:
    included = set()
    candidates = set(graph.keys())

    while candidates:
        v = random.sample(list(candidates), 1)[0]
        # Only add v if none of its neighbors are already included
        if not any(neigh in included for neigh in graph[v]):
            included.add(v)
        # Remove v and all its neighbors from candidates
        candidates.remove(v)
        for neigh in graph[v]:
            candidates.discard(neigh)

    # Local improvement: try to swap out vertices for pairs of their neighbors
    improved = True
    while improved:
        improved = False
        for v in list(included):
            neighbors = set(graph[v])
            # Only consider pairs of neighbors not already in the independent set
            neighbor_pairs = [(u, w) for u in neighbors for w in neighbors if u < w]
            for u, w in neighbor_pairs:
                if u in included or w in included:
                    continue
                # Check if u and w are not adjacent to any other included vertex (except v)
                if any(x in included and x != v for x in graph[u]):
                    continue
                if any(x in included and x != v for x in graph[w]):
                    continue
                # Check u and w are not neighbors of each other
                if w in graph[u] or u in graph[w]:
                    continue
                # If all checks pass, perform the swap
                included.remove(v)
                included.add(u)
                included.add(w)
                improved = True
                break
            if improved:
                break

    # Return the induced subgraph on the independent set
    return {node: graph[node] for node in included}

