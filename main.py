from typing import List

from north_west import apply_nw
from russel import RusselApproximation
from vogel import vogels_approximation


def custom_input():
    vector_s = [float(i) for i in input("Enter the supply vector S: ").split()]
    matrix_c = []
    print("Enter rows of cost matrix C line by line")
    for i in range(3):
        row = list(map(float, input().split()))
        matrix_c.append(row)
    vector_d = [float(i) for i in input("Enter the demand vector D: ").split()]
    return vector_s, matrix_c, vector_d


def format_cell(value):
    return "-" if value == "-" else f"{value:.0f}"


def print_initial_matrix(vector_s, matrix_c, vector_d):
    # Column widths to ensure alignment
    col_widths = [13] * (len(vector_d) + 2)

    # Headers for Destination and Supply
    print(" " * col_widths[0] + " ".join([f"{j + 1:^{col_widths[j + 1]}}" for j in range(len(vector_d))]) + "  Supply")

    # Separator line
    print("-" * sum(col_widths))

    # Print each row with Source labels ("A1", "A2", etc.) and Supply column
    for i, row in enumerate(matrix_c):
        row_str = f"A{i + 1}".ljust(col_widths[0])  # Label for source row
        for j, cost in enumerate(row):
            cell = format_cell(cost)
            row_str += f"{cell:^{col_widths[j + 1]}}"
        row_str += f"{vector_s[i]:^{col_widths[-1]}.0f}"  # Supply value with aligned width
        print(row_str)

    # Separator line before Demand row
    print("-" * sum(col_widths))

    # Print Demand row with aligned demand values
    demand_str = "Demand".ljust(col_widths[0])
    demand_str += "".join(f"{int(d):^{col_widths[j + 1]}}" for j, d in enumerate(vector_d))
    print(demand_str)


def print_solution(solution: List[List[float]]) -> None:
    col_widths = [max(len(str(item)) for item in col) for col in zip(*solution)]
    for row in solution:
        print("".join(f"{str(item):<{col_widths[i]}}  " for i, item in enumerate(row)))


def main():
    supply, table_content, demand = custom_input()
    print_initial_matrix(supply, table_content, demand)

    apply_nw(supply[:], table_content[:], demand[:])

    print()
    print("Vectors of Initial Basic Feasible Solution (x0) using Vogel's Approximation Method:")

    vogel_solution = vogels_approximation(supply, table_content, demand)
    print_solution(vogel_solution)

    print()
    print("Vectors of Initial Basic Feasible Solution (x0) using Russel's Approximation Method:")

    russel = RusselApproximation(table_content, supply, demand)
    russel_solution = russel.get_table_solution()
    print_solution(russel_solution)


if __name__ == "__main__":
    main()
