from itertools import count
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
        self.u: List[float] = list()
        self.v: List[float] = list()
        self._u_v_indices: Set[Tuple[int, int]] = set()
        self.deltas: Set[Delta] = set()
        self.solution: Dict[Delta, float] = dict()

    def _define_u(self) -> None:
        self.u.clear()

        for i in range(len(self.supply)):
            current_index: Tuple[int, int] = (0, 0)
            current_u_i: float = -INFINITY

            for j in range(len(self.demand)):
                if current_u_i < self.table_content[i][j]:
                    current_u_i = self.table_content[i][j]
                    current_index = (i, j)

            self.u.append(current_u_i)
            self._u_v_indices.add(current_index)

    def _define_v(self) -> None:
        self.v.clear()

        for j in range(len(self.demand)):
            current_index: Tuple[int, int] = (0, 0)
            current_v_j: float = -INFINITY

            for i in range(len(self.supply)):
                if current_v_j < self.table_content[i][j]:
                    current_v_j = self.table_content[i][j]
                    current_index = (i, j)

            self.v.append(current_v_j)
            self._u_v_indices.add(current_index)

    def define_u_v(self) -> None:
        self._u_v_indices.clear()
        self._define_v()
        self._define_u()

    def define_deltas(self) -> None:
        self.deltas.clear()
        for i in range(len(self.supply)):
            for j in range(len(self.demand)):

                if (i, j) in self._u_v_indices:
                    continue

                current_delta: Delta = Delta(
                    c=self.table_content[i][j],
                    u_i=self.u[i],
                    v_j=self.v[j],
                    i=i, j=j
                )
                self.deltas.add(current_delta)

    def remove_row(self, i: int) -> None:
        self.table_content.pop(i)
        self.supply.pop(i)

    def remove_column(self, j: int) -> None:
        for i in range(len(self.supply)):
            self.table_content[i].pop(j)
        self.demand.pop(j)

    def add_solution(self, basic_variable: Delta, amount: float) -> None:
        self.solution[basic_variable] = amount

        self.supply[basic_variable.i] -= amount
        self.demand[basic_variable.j] -= amount

        if self.supply[basic_variable.i] == 0:
            self.remove_row(basic_variable.i)

        if self.demand[basic_variable.j] == 0:
            self.remove_column(basic_variable.j)

    def define_basic_variable(self) -> None:
        basic_variable: Delta = min(self.deltas)
        amount: float = min(
            self.supply[basic_variable.i],
            self.demand[basic_variable.j]
        )
        self.add_solution(basic_variable, amount)

    def define_last_basic_variables(self) -> None:
        i_last, j_last = 0, 0
        while True:
            if len(self.table_content) == 0:
                break
            basic_variable = Delta(
                c=self.table_content[i_last][j_last],
                u_i=self.u[i_last],
                v_j=self.v[j_last],
                i=i_last, j=j_last
            )
            amount: float = min(
                self.supply[basic_variable.i],
                self.demand[basic_variable.j]
            )
            self.add_solution(basic_variable, amount)

    def find_solution(self):
        while True:
            self.define_u_v()
            self.define_deltas()
            if len(self.deltas) == 0:
                self.define_last_basic_variables()
                break
            self.define_basic_variable()


def main():
    table_content = [
        [30.0, 27.0, 53.0, 38.0],
        [47.0, 51.0, 29.0, 64.0],
        [49.0, 36.0, 15.0, 11.0],
    ]
    supply = [13.0, 42.0, 8.0]
    demand = [2.0, 12.0, 4.0, 45.0]
    russel = RusselApproximation(
        table_content,
        supply,
        demand
    )
    russel.find_solution()
    print(russel.solution)
    print(russel.table_content)
    print(russel.supply)
    print(russel.demand)
    pass


if __name__ == '__main__':
    main()
