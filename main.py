from mis_functions import exact_mis, greedy_mis, random_mis
from data_gen import generate_graph, write_graph, read_graph
import time as t
import random

def find_time(func, graph):
    start = t.perf_counter()
    mis = func(graph)
    end = t.perf_counter()
    return end - start, mis

def test_time_metrics(n, e):
    
    exact_times = []
    greedy_times = []
    random_times = []
    for _ in range(5):
        graph = generate_graph(n, e)
        exact_time, exact = find_time(exact_mis, graph)
        exact_times.append(exact_time)
        greedy_time, greedy = find_time(greedy_mis, graph)
        greedy_times.append(greedy_time)
        random_time, rand = find_time(random_mis, graph)
        random_times.append(random_time)
    print(f"For a graph with {n} vertices, and {e} edges, exact finished with an average time of {find_avg(exact_times)}, and a size of {len(exact)}")
    print(f"For a graph with {n} vertices, and {e} edges, greedy finished with an average time of {find_avg(greedy_times)}, and a size of {len(greedy)}")
    print(f"For a graph with {n} vertices, and {e} edges, random finished with an average time of {find_avg(random_times)}, and a size of {len(rand)}")

def find_avg(lyst):
    total = 0
    for item in lyst:
        total += item
    return total / len(lyst)



def main():
    """
    my_dict = {
                "1": set(["2", "4"]),
                "2": set(["1", "5", "3"]),
                "3": set(["2", "6"]),
                "4": set(["1", "5", "7"]),
                "5": set(["2", "4", "6", "8"]),
                "6": set(["3", "5", "9"]),
                "7": set(["4", "8"]),
                "8": set(["7", "5", "9"]),
                "9": set(["8", "6"])
            }
    mis = exact_mis(my_dict)
    greed_mis = greedy_mis(my_dict)
    print(mis)
    print(greed_mis)
    """
    random.seed(42)
    test_time_metrics(25, 60)


if __name__ == "__main__":
    main()

