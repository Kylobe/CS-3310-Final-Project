import csv
import random
import time as t
from mis_functions import exact_mis, greedy_mis, random_improve
from data_gen import generate_graph


def find_time(func, graph):
    start = t.perf_counter()
    mis = func(graph)
    end = t.perf_counter()
    return end - start, mis


def find_avg(lyst):
    return sum(lyst) / len(lyst)


def test_time_metrics(n, e):
    """
    Runs exact, greedy, and random MIS 5 times on fresh graphs with n vertices, e edges.
    Returns a single 'pivot' row:

    (n, e,
     exact_avg_time, exact_size,
     greedy_avg_time, greedy_size,
     random_avg_time, random_size)
    """

    exact_times = []
    greedy_times = []
    random_times = []

    exact_size = None
    greedy_size = None
    random_size = None

    for _ in range(5):
        graph = generate_graph(n, e)

        exact_time, exact = find_time(exact_mis, graph)
        exact_times.append(exact_time)
        exact_size = len(exact)

        greedy_time, greedy = find_time(greedy_mis, graph)
        greedy_times.append(greedy_time)
        greedy_size = len(greedy)

        random_time, rand = find_time(random_improve, graph)
        random_times.append(random_time)
        random_size = len(rand)

    exact_avg = round(find_avg(exact_times), 5)
    greedy_avg = round(find_avg(greedy_times), 5)
    random_avg = round(find_avg(random_times), 5)

    print(f"For a graph with {n} vertices, and {e} edges, exact finished with an average time of {exact_avg}, and a size of {exact_size}")
    print(f"For a graph with {n} vertices, and {e} edges, greedy finished with an average time of {greedy_avg}, and a size of {greedy_size}")
    print(f"For a graph with {n} vertices, and {e} edges, random finished with an average time of {random_avg}, and a size of {random_size}")

    return (
        n,
        e,
        exact_avg,
        exact_size,
        greedy_avg,
        greedy_size,
        random_avg,
        random_size,
    )


def main():
    random.seed(42)
    all_rows = []

    for n in range(5, 26, 5):
        e = 2 * n
        row = test_time_metrics(n, e)
        all_rows.append(row)

    # Write pivot-style CSV
    with open("mis_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vertices",
            "edges",
            "exact_time",
            "exact_size",
            "greedy_time",
            "greedy_size",
            "random_time",
            "random_size",
        ])
        writer.writerows(all_rows)

    print("\nCSV file 'mis_pivot_results.csv' written successfully!")


if __name__ == "__main__":
    main()
