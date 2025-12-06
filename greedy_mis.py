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