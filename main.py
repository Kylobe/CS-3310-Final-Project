from exact_mis import exact_mis


def main():
    my_dict = {
                "1": ["2", "4"],
                "2": ["1", "5", "3"],
                "3": ["2", "6"],
                "4": ["1", "5", "7"],
                "5": ["2", "4", "6", "8"],
                "6": ["3", "5", "9"],
                "7": ["4", "8"],
                "8": ["7", "5", "9"],
                "9": ["8", "6"]
            }
    mis = exact_mis(my_dict)
    print(mis)


if __name__ == "__main__":
    main()

