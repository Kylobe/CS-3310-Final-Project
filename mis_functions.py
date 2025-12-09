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

def greedy_minor_optim(graph: Mapping[int, Iterable[int]]) -> Dict[int, Iterable[int]]:
    # graph: dict[node, list_of_neighbors]
    remaining = set(graph.keys())
    mis_nodes = set()

    while remaining:
        # choose node with minimum degree *within remaining*
        def degree_in_remaining(u):
            return sum(1 for v in graph[u] if v in remaining)

        if len(remaining) <= 25:
            mis_nodes = mis_nodes | set(exact_mis({ key: graph[key] for key in remaining }).keys())
        least_node = min(remaining, key=degree_in_remaining)

        # add to MIS
        mis_nodes.add(least_node)

        # remove it and its neighbors from remaining
        remaining.remove(least_node)
        for neighbor in graph[least_node]:
            remaining.discard(neighbor)

    local_improve(mis_nodes, graph)
    return {node: graph[node] for node in mis_nodes}

def local_improve(independent_set: set[int], graph: Mapping[int, Iterable[int]]):
    improved = True
    while improved:
        improved = False
        for v in list(independent_set):
            neighbors = set(graph[v])
            # Only consider pairs of neighbors not already in the independent set
            neighbor_pairs = [(u, w) for u in neighbors for w in neighbors if u < w]
            for u, w in neighbor_pairs:
                if u in independent_set or w in independent_set:
                    continue
                # Check if u and w are not adjacent to any other included vertex (except v)
                if any(x in independent_set and x != v for x in graph[u]):
                    continue
                if any(x in independent_set and x != v for x in graph[w]):
                    continue
                # Check u and w are not neighbors of each other
                if w in graph[u] or u in graph[w]:
                    continue
                # If all checks pass, perform the swap
                independent_set.remove(v)
                independent_set.add(u)
                independent_set.add(w)
                improved = True
                break
            if improved:
                break

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

    local_improve(included, graph)
    return {node: graph[node] for node in included}

def merge_independent_sets(left_mis: set[int],
                           right_mis: set[int],
                           true_graph: Mapping[int, set[int]]) -> set[int]:
    """
    Merge two independent sets into a larger independent set.
    If a conflict occurs, drop the higher-degree vertex (in true_graph).
    """
    merged = set(left_mis) | set(right_mis)

    changed = True
    while changed:
        changed = False
        for v in list(merged):
            for u in true_graph[v]:
                if u in merged and u != v:
                    # break the conflict: keep the lower-degree vertex
                    if len(true_graph[v]) > len(true_graph[u]):
                        merged.remove(v)
                    else:
                        merged.remove(u)
                    changed = True
                    break
            if changed:
                break

    return merged


def recursive_mis(graph: Mapping[int, set[int]],
                  true_graph: Mapping[int, set[int]]) -> set[int]:
    """
    Recursive MIS heuristic:
    - Split the vertex set into two halves
    - Build induced subgraphs on each half
    - Recurse on each side
    - Solve small subgraphs exactly
    - Merge the resulting independent sets
    """
    n = len(graph)
    if n == 0:
        return set()
    if n <= 20:
        vertices = set(graph.keys())
        induced = {
            v: {u for u in true_graph[v] if u in vertices}
            for v in vertices
        }
        return exact_mis(induced)

    nodes = list(graph.keys())
    left_nodes  = set(nodes[len(nodes)//2:])
    right_nodes = set(nodes[:len(nodes)//2])

    # Build induced subgraphs on each side
    left_graph = {
        v: {u for u in graph[v] if u in left_nodes}
        for v in left_nodes
    }
    right_graph = {
        v: {u for u in graph[v] if u in right_nodes}
        for v in right_nodes
    }

    # Recurse
    left_mis = recursive_mis(left_graph, true_graph)
    right_mis = recursive_mis(right_graph, true_graph)

    # Merge the two independent sets
    merged = merge_independent_sets(set(left_mis.keys()), set(right_mis.keys()), true_graph)
    return { key: graph[key] for key in merged }
