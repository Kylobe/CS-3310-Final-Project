from typing import Mapping, Iterable, Dict
import random


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
