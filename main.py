import csv
import random
import time as t
from mis_functions import exact_mis, greedy_mis, random_improve, greedy_minor_optim, recursive_mis, greedy_with_exact
from data_gen import generate_graph
import sys


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
    greedy_exact_times = []
    greedy_opt_times = []
    recur_times = []

    exact_size = None
    greedy_size = None
    random_size = None
    include_exact = n <= 20

    for _ in range(5):
        graph = generate_graph(n, e)

        if include_exact:
            exact_time, exact = find_time(exact_mis, graph)
            exact_times.append(exact_time)
            exact_size = len(exact)
        else:
            exact_time, exact, exact_size = (None, None, None)

        greedy_time, greedy = find_time(greedy_mis, graph)
        greedy_times.append(greedy_time)
        greedy_size = len(greedy)

        random_time, rand = find_time(random_improve, graph)
        random_times.append(random_time)
        random_size = len(rand)

        greedy_opt_time, greedy_opt = find_time(greedy_minor_optim, graph)
        greedy_opt_times.append(greedy_opt_time)
        greedy_opt_size = len(greedy_opt)

        greedy_exact_time, greedy_exact = find_time(greedy_with_exact, graph)
        greedy_exact_times.append(greedy_exact_time)
        greedy_exact_size = len(greedy_exact)

        recur_time, recur = find_time(recursive_mis, graph)
        recur_times.append(recur_time)
        recur_size = len(recur)

    if exact_times:
        exact_avg = round(find_avg(exact_times), 5)
    else:
        exact_avg = None
    greedy_avg = round(find_avg(greedy_times), 5)
    random_avg = round(find_avg(random_times), 5)
    greedy_opt_avg = round(find_avg(greedy_opt_times), 5)
    recur_avg = round(find_avg(recur_times), 5)
    greedy_exact_avg = round(find_avg(greedy_exact_times), 5)

    print(f"finished testing graph of size: {n}")

    return (
        n,
        e,
        exact_avg,
        exact_size,
        greedy_avg,
        greedy_size,
        random_avg,
        random_size,
        greedy_opt_avg,
        greedy_opt_size,
        greedy_exact_avg,
        greedy_exact_size,
        recur_avg,
        recur_size
    )


def main():
    sys.setrecursionlimit(10000)
    random.seed(42)
    all_rows = []

    for n in range(5, 26, 5):
        e = 2 * n
        row = test_time_metrics(n, e)
        all_rows.append(row)

    for n in range(1000, 5001, 1000):
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
            "greedy_local_improve_time",
            "greedy_local_improve_size",
            "greedy_brute_force_time",
            "greedy_brute_force_size",
            "recursive_time",
            "recursive_size"
        ])
        writer.writerows(all_rows)

    print("\nCSV file 'mis_pivot_results.csv' written successfully!")


if __name__ == "__main__":
    main()
