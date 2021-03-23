def cube(number) -> int:
    """
    Returns cube of a number
    :param number: takes a number
    :return: returns cube of a number
    """
    return number * number * number


def square(number) -> int:
    """
    Returns square of a number
    :param number: takes a number
    :return: returns square of number
    """
    return number * number


def main():
    """
    Prints number, its square and its cube for numbers from 1 to 10
    :return: None
    """
    print("-" * 22)
    print("| Number| Square| Cube|")
    print("-" * 22)
    for i in range(1, 11):
        print('|', end="")
        print(str(i).rjust(7), end="|")
        print(str(square(i)).rjust(7), end="|")
        print(str(cube(i)).rjust(5), end="|\n")
    print("-" * 22)
    return


main()
# Calling main function

# Output
# ----------------------
# | Number| Square| Cube|
# ----------------------
# |      1|      1|    1|
# |      2|      4|    8|
# |      3|      9|   27|
# |      4|     16|   64|
# |      5|     25|  125|
# |      6|     36|  216|
# |      7|     49|  343|
# |      8|     64|  512|
# |      9|     81|  729|
# |     10|    100| 1000|
# ----------------------
