# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1. If the stone is
# engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits
# are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new
# numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.) If none of the other rules apply,
# the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
from collections import deque
from dataclasses import dataclass
from typing import Self
import math
from icecream import ic
from pathlib import Path
from pytictoc import TicToc

t = TicToc()

stones = deque()
stones.extend(map(int, Path("input.txt").read_text().split(" ")))
ic(stones)
for tt in range(25):
  t.tic()
  new_stones = deque()
  for i in stones:
    if i == 0:
      new_stones.append(1)
    elif len(str_i := str(i)) % 2 == 0:
      mid_point = len(str_i) // 2
      new_stones.append(int(str_i[:mid_point]))
      new_stones.append(int(str_i[mid_point:]))
    else:
      new_stones.append(i * 2024)
  stones = new_stones
  ic(tt)
  t.toc()
print(len(stones)) # 175006
