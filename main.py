from typing import Dict, Set

from exact_mis import exact_mis
from greedy_mis import greedy_mis
from local_improve import random_improve


def main() -> None:
    my_dict: Dict[str, Set[str]] = {
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
    approx_mis = greedy_mis(my_dict)
    random_improve_mis = random_improve(my_dict)
    print(f"Exact MIS cardinality: {len(mis)}\n\t{mis}\n")
    print(f"Approximation MIS cardinality: {len(approx_mis)}\n\t{approx_mis}\n")
    print(f"Random Improve MIS cardinality: {len(random_improve_mis)}\n\t{random_improve_mis}\n")
    
if __name__ == "__main__":
    main()

