from collections import deque
from dataclasses import dataclass
from pathlib import Path
from pyprojroot.here import here
from icecream import ic
import matplotlib.pyplot as plt
from pprint import pp

ic.enable()

def main(file: Path, n_blinked: int):
  #region build adj list
  adj_list: dict[int, list[int]] = {}
  root_stones = curr_stones = deque(map(int, Path(file).read_text().split(" ")))
  for i in range(n_blinked):
    next_stones = deque()
    for stone in curr_stones:
      if stone in adj_list: continue # found loop
      #region conditions
      if stone == 0:
        adj_list[0] = [1]
        next_stones.append(1)
      elif len(str_stone := str(stone)) % 2 == 0:
        mid_point = len(str_stone) // 2
        left = int(str_stone[:mid_point])
        right = int(str_stone[mid_point:])
        adj_list[stone] = [left, right]
        next_stones.append(left)
        next_stones.append(right)
      else:
        new_stone = stone * 2024
        adj_list[stone] = [new_stone]
        next_stones.append(new_stone)
      #endregion
    if len(next_stones) == 0:
      print(f"found complete graph consisting of {len(adj_list)} nodes in {i} iterations")
      break
    curr_stones = next_stones
  else:
    print(f"incomplete graph consisting of {len(adj_list)} nodes ({n_blinked} iterations)")
  #endregion
  pp(adj_list)



  # #region find first loop
  # root = root_stones[0]
  # visited = dict()
  # nodes_that_spawned_more = deque()
  # i = 0
  # while True:
  #   i += 1
  #   if root in visited:
  #     break
  #   visited[root] = i
  #   children = adj_list[root]
  #   if len(children) > 1:
  #     nodes_that_spawned_more.append(root)
  #   root = adj_list[root][0]
  # pp(visited)
  # ic(nodes_that_spawned_more)
  # print(f"found loop of {i - visited[root]} nodes at node={root}")
  # print(f"This root node spawned {len(nodes_that_spawned_more)} children, {
  # len(nodes_that_spawned_more) - len(list(filter(lambda x: x in nodes_that_spawned_more and visited[x] > visited[root], nodes_that_spawned_more)))
  # } of which are outside the loop")
  # """
  #   This would result in an out of:
  #   def out_of_stone(stone, depth = 75):
  #     return 1 (last number) +
  #       + out_of_stone(stone) of stones outside of the loop found, for each stone, with depth = 75 - visited[stone]
  #       + out_of_stone(stone) of stones inside of the loop found, for each stone, times the number that that stone is repeated in the loop (eg 4048, the first number after the loop,
  # """
  # #endregion
  #region calculate out
  @dataclass
  class Out:
    val: int = 0
  out = Out()
  def transverse(stone, depth = 0):
    if depth == n_blinked:
      out.val += 1
      return
    for child in adj_list[stone]:
      transverse(child, depth+1)
  #for root in root_stones:
  #  ic(root)
  #  transverse(root)
  #endregion
  return out.val

if __name__ == '__main__':
  out = ic(main(file = here("2024/day11/test.txt"), n_blinked = 75))
  print(f"{out=}")