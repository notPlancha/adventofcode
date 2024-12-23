from collections import deque, defaultdict
from more_itertools import pairwise
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from pyprojroot.here import here
from icecream import ic
import matplotlib.pyplot as plt
from dataclasses import dataclass
from pytictoc import TicToc
import functools

def node_on_graph(g, node):
  return node in g


last_of_level: dict[int, int] = defaultdict(lambda: -1)
t = TicToc()


def add_node(g, node, y_level, new_stones_list):
  if node not in g:
    last_of_level[y_level] += 1
    x = last_of_level[y_level]
    g.add_node(node, pos=(x, -y_level))
    new_stones_list.append(node)
    # Invert the y position by multiplying it with -1
    # add node to the graph at the given y_level and a new x, right to the previous node


def main(viz=False, file_name=here("2024/day11/input.txt"), times_to_blink=75):
  g = nx.DiGraph()
  stones = deque()
  stones.extend(map(int, Path(file_name).read_text().split(" ")))

  # region add root stones
  for stone in stones:
    add_node(g, stone, 0, deque())

  # endregion
  for blinked in range(times_to_blink):
    t.tic()
    new_stones = deque()
    # region create new stones and add them to graph and join to previous nodes
    for i in stones:
      if i == 0:
        add_node(g, 1, blinked + 1, new_stones)
        g.add_edge(0, 1)
      elif len(str_i := str(i)) % 2 == 0:
        mid_point = len(str_i) // 2
        left = int(str_i[:mid_point])
        right = int(str_i[mid_point:])
        if left == right:
          # mark i node
          g.nodes[i]["color"] = "red"
        add_node(g, left, blinked + 1, new_stones)
        g.add_edge(i, left)
        add_node(g, right, blinked + 1, new_stones)
        g.add_edge(i, right)
      else:
        new_stone = i * 2024
        add_node(g, new_stone, blinked + 1, new_stones)
        g.add_edge(i, new_stone)
    # endregion
    stones = new_stones
    t.toc(f"{blinked=}, ")

  # region Visualize the graph
  pos = nx.get_node_attributes(g, "pos")
  if viz:
    plt.figure(figsize=(10, 10))
    # find out colors
    colors = [g.nodes[n].get("color", "skyblue") for n in g.nodes]
    nx.draw(g, pos=pos, with_labels=True, node_size=1000, font_size=10, node_color=colors, edge_color="gray")
    plt.title("Graph Visualization")
    plt.savefig(here("2024/day11/graph.pdf"))
    plt.show()
  #endregion

  #region transverse
  roots = list(map(int, Path(file_name).read_text().split(" ")))
  ic(roots)

  @dataclass
  class Out:
    value: int

  out = Out(0)

  @functools.cache
  def sucessors(node):
    return g.successors(node)

  def transverse(g, root, depth, td=times_to_blink, n=out):
    if depth == td:
      n.value += 1
      return
    depth += 1
    if g.nodes[root].get("color") == "red":
      transverse(g, next(g.successors(root)), depth, td, n)
    for node in g.successors(root):
      transverse(g, node, depth, td, n)
    return

  for root in roots:
    t.tic()
    depth = 0
    transverse(g, root, depth)
    t.toc(f"{root=}, {out.value=},")
  print(out.value)
  # print(final_stones)
  #endregion


if __name__ == '__main__':
  main(viz=False, file_name=here("2024/day11/test.txt"), times_to_blink=75)
