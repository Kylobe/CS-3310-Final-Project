from exact_mis import exact_mis
from greedy_mis import greedy_mis


def main():
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
    aprox_mis = greedy_mis(my_dict)
    print(mis)
    print(aprox_mis)


if __name__ == "__main__":
    main()

