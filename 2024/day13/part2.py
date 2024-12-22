from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple
import pprint
import pulp
import sympy
from icecream import ic
from pulp import *
from pytictoc import TicToc
from sympy.core.numbers import int_valued

ic.configureOutput(argToStringFunction=lambda x: pprint.pformat(x, sort_dicts=False))  # icecream bug #199
t = TicToc()
ic.disable()

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
  machines = load_data("input.txt")
  out = 0
  t.tic()
  for i, machine in enumerate(machines):
    ic(i)
    A, B, p = machine.A, machine.B, machine.prize
    A: Button
    B: Button
    p: Prize

    # equation is AX*na + BX*nb = px
    na, nb = sympy.symbols("na nb", integer=True)
    d = ic(sympy.solve([  # if too slow, use nsolve
      A.x * na + B.x * nb - (p.x + 1e13),
      A.y * na + B.y * nb - (p.y + 1e13),
    ], [na, nb], dict=True))
    ic(d)
    if len(d) > 0:
      # assert len(d) == 1  # Can calculate best one if needed but input doesnt have any example of this
      out += 3 * d[0][na] + 1 * d[0][nb]
  t.toc()
  print(out) # 108528956728655
