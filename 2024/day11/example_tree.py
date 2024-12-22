from pathlib import Path

import graphviz
from graphviz import Digraph

g = Digraph("stones")
stones = list(map(int, Path("test.txt").read_text().split(" ")))


def treat_stone(stone: int, from_node=None, blinked=0):
  if blinked >= 6:
    return
  g.node(self_node := f"{stone}_{blinked}")
  if from_node is not None: g.edge(f"{from_node}_{blinked - 1}", self_node)
  if stone == 0:
    treat_stone(1, stone, blinked=blinked + 1)
    return
  str_stone = str(stone)
  if len(str_stone) % 2 == 0:
    mid_point = len(str_stone) // 2
    treat_stone(int(str_stone[mid_point:]), stone, blinked=blinked + 1)
    treat_stone(int(str_stone[:mid_point]), stone, blinked=blinked + 1)
  else:
    treat_stone(stone * 2024, stone, blinked=blinked + 1)
  return


for stone in stones:
  treat_stone(stone)

g.render("graph", view=True)
