from __future__ import annotations

from collections import deque, Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from pyprojroot.here import here
from icecream import ic
import matplotlib.pyplot as plt
from pprint import pp
from functools import cache, lru_cache


stones = deque()
stones.extend(map(int, Path(here("2024/day11/input.txt")).read_text().split(" ")))

@cache
def t(stone) -> tuple[int] | tuple[int, int]:
  if stone == 0:
    return (1, )
  elif len(str_stone := str(stone)) % 2 == 0:
    mid_point = len(str_stone) // 2
    return int(str_stone[:mid_point]), int(str_stone[mid_point:])
  else:
    return (stone * 2024, )


curr_counter = Counter(stones)
for _ in range(75):
  next_counter = defaultdict(lambda: 0)
  for stone, times in curr_counter.items():
    new_stones = t(stone)
    for stone in new_stones:
      next_counter[stone] += times
  curr_counter = next_counter

print(sum(curr_counter.values()))
