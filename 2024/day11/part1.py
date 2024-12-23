from collections import deque
from dataclasses import dataclass
from typing import Self
import math
from icecream import ic
from pathlib import Path
from pytictoc import TicToc

t = TicToc()
ic.disable()

stones = deque()
stones.extend(map(int, Path("test.txt").read_text().split(" ")))
ic(stones)
t.tic()
for tt in range(25):
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
print(stones)
print(len(stones))  # 175006
