import csv
import random
import time as t
from mis_functions import exact_mis, greedy_mis, random_improve, greedy_minor_optim, recursive_mis, greedy_with_exact
from data_gen import generate_graph
import sys
import pandas as pd
import matplotlib.pyplot as plt


def plot_mis_times(csv_file="mis_results.csv"):
    """
    Reads the pivot CSV produced by MIS experiments and plots
    the runtime of each algorithm vs. number of vertices.
    """

    # Load CSV
    df = pd.read_csv(csv_file)

    # Keep only rows where timing exists
    # (exact_time is None for large graphs)
    x = df["vertices"]

    # Build plot
    plt.figure(figsize=(12, 7))

    # Only plot exact where it exists
    plt.plot(x, df["exact_time"], marker="o", label="Exact MIS")

    plt.plot(x, df["greedy_time"], marker="o", label="Greedy MIS")
    plt.plot(x, df["random_time"], marker="o", label="Random Improve")
    plt.plot(x, df["greedy_local_improve_time"], marker="o",
             label="Greedy Local Improve")
    plt.plot(x, df["greedy_brute_force_time"], marker="o",
             label="Greedy + Exact Improve")
    plt.plot(x, df["recursive_time"], marker="o",
             label="Recursive MIS")

    # Labels and title
    plt.xlabel("Number of Vertices (n)", fontsize=14)
    plt.ylabel("Average Time (seconds)", fontsize=14)
    plt.title("MIS Algorithm Runtime Comparison", fontsize=16)

    # Log-scale Y axis if needed (useful when Exact blows up)
    plt.yscale('log')

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig("time_plot.png")
    plt.close()

def plot_mis_sizes(csv_file="mis_results.csv"):
    """
    Reads the pivot CSV produced by MIS experiments and plots
    the size of the MIS found by each algorithm vs. number of vertices.
    """

    # Load CSV
    df = pd.read_csv(csv_file)

    x = df["vertices"]

    plt.figure(figsize=(12, 7))

    # Only plot exact where it exists (small n)
    plt.plot(x, df["exact_size"], marker="o", label="Exact MIS")

    plt.plot(x, df["greedy_size"], marker="o", label="Greedy MIS")
    plt.plot(x, df["random_size"], marker="o", label="Random Improve")
    plt.plot(x, df["greedy_local_improve_size"], marker="o",
             label="Greedy Local Improve")
    plt.plot(x, df["greedy_brute_force_size"], marker="o",
             label="Greedy + Exact Improve")
    plt.plot(x, df["recursive_size"], marker="o",
             label="Recursive MIS")

    plt.xlabel("Number of Vertices (n)", fontsize=14)
    plt.ylabel("MIS Size (|S|)", fontsize=14)
    plt.title("MIS Algorithm Solution Size Comparison", fontsize=16)

    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()

    plt.savefig("size_plot.png")
    plt.close()


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
    n = 5120
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
    plot_mis_times()
    plot_mis_sizes()
