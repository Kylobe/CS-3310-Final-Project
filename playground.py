from mis_functions import recursive_mis, exact_mis, greedy_mis, random_improve, is_independent_set, greedy_minor_optim
from data_gen import generate_graph
import random
import sys



def main():
    random.seed(42)
    sys.setrecursionlimit(10000)
    graph = generate_graph(1000, 2000)
    recur_mis = recursive_mis(graph, graph)
    print("recur done")
    greed_opt = set(greedy_minor_optim(graph).keys())
    greed = set(greedy_mis(graph).keys())
    print("greedy done")
    rand = set(random_improve(graph).keys())
    print("random done")
    print(len(greed_opt))
    print(len(greed))
    print(len(rand))
    print(len(recur_mis))


if __name__ == "__main__":
    main()