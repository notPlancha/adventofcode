from collections import deque
from dataclasses import dataclass
from pathlib import Path

from icecream import ic
from pytictoc import TicToc

t = TicToc()
ic.enable()

stones = list(map(int, Path("test.txt").read_text().split(" ")))
ic(stones)


@dataclass()
class Out:
  value: int


out = Out(len(stones))
l = deque()

def treat_stone(stone: int, blinked=0):
  if blinked >= 6 :
    l.append(stone)
    return
  ic(stone)
  if stone == 0:
    treat_stone(1, blinked=blinked + 1)
    return
  str_stone = str(stone)
  if len(str_stone) % 2 == 0:
    out.value += 1
    mid_point = len(str_stone) // 2
    treat_stone(int(str_stone[mid_point:]), blinked=blinked + 1)
    treat_stone(int(str_stone[:mid_point]), blinked=blinked + 1)
  else:
    treat_stone(stone * 2024, blinked=blinked + 1)
  return


for stone in stones:
  t.tic()
  treat_stone(stone)
  t.toc()
print(out)
