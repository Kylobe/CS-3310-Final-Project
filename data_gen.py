import random



def generate_graph(n, e):
    if n <= 1:
        raise ValueError
    if e > n * (n - 1) // 2:
        raise ValueError
    graph = { key: set() for key in range(n)}
    nodes = list([i for i in range(n)])
    for _ in range(e):
        first_node = random.choice(nodes)
        second_node = random.choice(nodes)
        max_attempts = 10000
        while first_node == second_node or (first_node in graph and second_node in graph[first_node]):
            max_attempts -= 1
            first_node = random.choice(nodes)
            second_node = random.choice(nodes)
            if max_attempts <= 0:
                raise ValueError
        if not first_node in graph:
            graph[first_node] = set([second_node])
        else:
            graph[first_node].add(second_node)
        if not second_node in graph:
            graph[second_node] = set([first_node])
        else:
            graph[second_node].add(first_node)
    return graph
        
def write_graph(path, graph):
    with open(path, 'w', encoding='utf-8') as file:
        for cur_node in graph:
            for neighbor in graph[cur_node]:
                cur_string = f"{cur_node} {neighbor}\n"
                file.write(cur_string)


def read_graph(path):
    graph = {}
    with open(path, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            first, second = line.split(" ")
            first, second = int(first), int(second)
            if not first in graph:
                graph[first] = set([second])
            else:
                graph[first].add(second)
    return graph




