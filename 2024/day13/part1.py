from pathlib import Path
from dataclasses import dataclass
from collections import namedtuple
import re

re_b = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
re_p = re.compile(r"Prize: X=(\d+), Y=(\d+)")

Button = namedtuple("Button", "x y")
Prize = namedtuple("Prize", "x y")


@dataclass
class Machine:
  @staticmethod
  def from_list(l: list[str]) -> "Machine":
    tuple(map(int, re_b.match(l[0]).group(1, 2)))
    return Machine(
      A=Button(*map(int, re_b.match(l[0]).group(1, 2))),
      B=Button(*map(int, re_b.match(l[1]).group(1, 2))),
      prize=Prize(*map(int, re_p.match(l[2]).group(1, 2))),
    )

  A: Button
  B: Button
  prize: Prize


def load_data() -> list[Machine]:
  machines = [section.splitlines() for section in Path("input.txt").read_text().split("\n\n")]
  return [Machine.from_list(i) for i in machines]

if __name__ == '__main__':
  machines = load_data()

