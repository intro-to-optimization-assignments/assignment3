from json.encoder import INFINITY
from typing import List, Tuple, Set, Dict

M: float = 1_000_000.0


class Delta:
    def __init__(
            self,
            c: float,
            u_i: float,
            v_j: float,
            i: int,
            j: int
    ) -> None:
        self.c = c
        self.u_i = u_i
        self.v_j = v_j
        self.i = i
        self.j = j
        self.delta = c - u_i - v_j

    def __lt__(self, other: 'Delta') -> bool:
        return self.delta < other.delta

    def __repr__(self) -> str:
        return f"((i={self.i}, j={self.j}): {self.c})"


class RusselApproximation:
    def __init__(
            self,
            table_content: List[List[float]],
            supply: List[float],
            demand: List[float]
    ) -> None:
        self.table_content = table_content
        self.supply = supply
        self.demand = demand
        self._u: List[float] = list()
        self._v: List[float] = list()
        self._u_v_indices: Set[Tuple[int, int]] = set()
        self._deltas: Set[Delta] = set()
        self.solution: Dict[Delta, float] = dict()
        self._closed_i: Set[int] = set()
        self._closed_j: Set[int] = set()

    def _define_u(self) -> None:
        self._u = [0.0 for _ in range(len(self.supply))]

        for i in range(len(self.supply)):
            if i in self._closed_i: continue

            current_index: Tuple[int, int] = (0, 0)
            current_u_i: float = -INFINITY

            for j in range(len(self.demand)):
                if j in self._closed_j: continue

                if current_u_i < self.table_content[i][j]:
                    current_u_i = self.table_content[i][j]
                    current_index = (i, j)

            self._u.append(current_u_i)
            self._u_v_indices.add(current_index)

    def _define_v(self) -> None:
        self._v = [0.0 for _ in range(len(self.demand))]

        for j in range(len(self.demand)):
            if j in self._closed_j: continue

            current_index: Tuple[int, int] = (0, 0)
            current_v_j: float = -INFINITY

            for i in range(len(self.supply)):
                if i in self._closed_i: continue

                if current_v_j < self.table_content[i][j]:
                    current_v_j = self.table_content[i][j]
                    current_index = (i, j)

            self._v.append(current_v_j)
            self._u_v_indices.add(current_index)

    def _define_u_v(self) -> None:
        self._u_v_indices.clear()
        self._define_v()
        self._define_u()

    def _define_deltas(self) -> None:
        self._deltas.clear()
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):

                if ((i, j) in self._u_v_indices
                        or i in self._closed_i
                        or j in self._closed_j
                ): continue

                current_delta: Delta = Delta(
                    c=self.table_content[i][j],
                    u_i=self._u[i],
                    v_j=self._v[j],
                    i=i, j=j
                )
                self._deltas.add(current_delta)

    def _add_solution(self, basic_variable: Delta, amount: float) -> None:
        self.solution[basic_variable] = amount

        self.supply[basic_variable.i] -= amount
        self.demand[basic_variable.j] -= amount

        if self.supply[basic_variable.i] == 0:
            self._closed_i.add(basic_variable.i)

        if self.demand[basic_variable.j] == 0:
            self._closed_j.add(basic_variable.j)

    def _define_basic_variable(self) -> None:
        basic_variable: Delta = min(self._deltas)
        amount: float = min(
            self.supply[basic_variable.i],
            self.demand[basic_variable.j]
        )
        self._add_solution(basic_variable, amount)

    def _define_last_basic_variables(self) -> None:
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):
                if len(self._closed_i) == len(self.supply) and len(self._closed_j) == len(self.demand):
                    break

                if i in self._closed_i or j in self._closed_j:
                    continue

                self._define_u_v()
                basic_variable = Delta(
                    c=self.table_content[i][j],
                    u_i=self._u[i],
                    v_j=self._v[j],
                    i=i, j=j
                )
                amount: float = min(
                    self.supply[basic_variable.i],
                    self.demand[basic_variable.j]
                )
                self._add_solution(basic_variable, amount)

    def find_solution(self):
        while True:
            self._define_u_v()
            self._define_deltas()
            if len(self._deltas) == 0:
                self._define_last_basic_variables()
                break
            self._define_basic_variable()

    def get_table_solution(self) -> List[List[float]]:
        self.find_solution()
        solution_table: List[List[float]] = [
            [0.0 for _ in range(len(self.demand))]
            for _ in range(len(self.supply))
        ]
        for basic_variable in self.solution:
            i = basic_variable.i
            j = basic_variable.j
            solution_table[i][j] = self.solution[basic_variable]

        return solution_table


def custom_input():
    vector_s = [float(i) for i in input("Enter the supply vector S: ").split()]
    matrix_c = []
    print("Enter rows of cost matrix C line by line")
    for i in range(3):
        row = list(map(float, input().split()))
        matrix_c.append(row)
    vector_d = [float(i) for i in input("Enter the demand vector D: ").split()]
    return vector_s, matrix_c, vector_d


def main():
    supply, table_content, demand = custom_input()
    russel = RusselApproximation(
        table_content,
        supply,
        demand
    )
    russel.find_solution()
    for row in russel.get_table_solution():
        print(*row)


if __name__ == '__main__':
    main()
