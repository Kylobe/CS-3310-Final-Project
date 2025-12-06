from mis_functions import exact_mis, greedy_mis
from data_gen import generate_graph, write_graph, read_graph


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
    for i in range(5):
        graph = generate_graph(10, 15)
        write_graph(f"graph_files\\small{i}.txt", graph)

    for i in range(5):
        graph = generate_graph(100, 300)
        write_graph(f"graph_files\\medium{i}.txt", graph)

    graph = generate_graph(100000, 1000000)
    write_graph("graph_files\\LargeGraph.txt", graph)



if __name__ == "__main__":
    main()

