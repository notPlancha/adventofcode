from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple

import pulp
from icecream import ic
from pulp import *
from pytictoc import TicToc

t = TicToc()
ic.enable()

re_b = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
re_p = re.compile(r"Prize: X=(\d+), Y=(\d+)")

class Button(NamedTuple):
  x: int
  y: int
class Prize(NamedTuple):
  x: int
  y: int


@dataclass
class Machine:
  @staticmethod
  def from_list(l: list[str]) -> "Machine":
    tuple(map(int, re_b.match(l[0]).group(1, 2)))
    return ic(Machine(
      A=Button(*map(int, re_b.match(l[0]).group(1, 2))),
      B=Button(*map(int, re_b.match(l[1]).group(1, 2))),
      prize=Prize(*map(int, re_p.match(l[2]).group(1, 2))),
    ))

  A: Button
  B: Button
  prize: Prize


def load_data(file_name) -> list[Machine]:
  machines = [section.splitlines() for section in Path(file_name).read_text().split("\n\n")]
  return [Machine.from_list(i) for i in machines]

if __name__ == '__main__':
  machines = load_data("test_inp.txt")
  out = 0
  t.tic()
  for i, machine in enumerate(machines):
    if i != 1: continue
    ic(i)
    A, B, p = machine.A, machine.B, machine.prize
    A: Button
    B: Button
    p: Prize

    # equation is AX*na + BX*nb = px
    # obj: lowerst tokens
    # tokens = na*3 + nb * 1
    na = LpVariable("na", 100, 1e14, cat=LpInteger)
    nb = LpVariable("nb", 100, 1e14, cat=LpInteger)
    prob = LpProblem(f"Machine_{i}", LpMinimize)
    prob += 3*na + 1*nb
    prob += A.x*na + B.x*nb == p.x + 1e13
    prob += A.y*na + B.y*nb == p.y + 1e13
    ic(prob)
    status = prob.solve(getSolver("GLPK_CMD"))
    ic(LpStatus[status], status)
    if status == 1: # Optimal found
      out += prob.objective.value()
  t.toc()
  print(out)