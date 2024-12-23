from collections import deque, defaultdict
from itertools import pairwise
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from pyprojroot.here import here
from icecream import ic
import matplotlib.pyplot as plt
from dataclasses import dataclass


def node_on_graph(g, node):
  return node in g


last_of_level: dict[int, int] = defaultdict(lambda: -1)


def add_node(g, node, y_level, new_stones_list):
  if node not in g:
    last_of_level[y_level] += 1
    x = last_of_level[y_level]
    g.add_node(node, pos=(x, -y_level))
    new_stones_list.append(node)
    # Invert the y position by multiplying it with -1
    # add node to the graph at the given y_level and a new x, right to the previous node


file_name = here("2024/day11/test.txt")
times_to_blink = 10

g = nx.DiGraph()
stones = deque()
stones.extend(map(int, Path(file_name).read_text().split(" ")))

# region add root stones
for stone in stones:
  add_node(g, stone, 0, deque())

# endregion

# test node_on_graph
ic(node_on_graph(g, 17))
assert node_on_graph(g, 17)

for blinked in range(times_to_blink):
  new_stones = deque()
  # region create new stones and add them to graph and join to previous nodes
  for i in stones:
    if i == 0:
      add_node(g, 1, blinked + 1, new_stones)
      g.add_edge(0, 1)
    elif len(str_i := str(i)) % 2 == 0:
      mid_point = len(str_i) // 2
      add_node(g, int(str_i[:mid_point]), blinked + 1, new_stones)
      g.add_edge(i, int(str_i[:mid_point]))
      g.add_edge(i, int(str_i[:mid_point]))
      add_node(g, int(str_i[mid_point:]), blinked + 1, new_stones)
      g.add_edge(i, int(str_i[mid_point:]))
    else:
      new_stone = i * 2024
      add_node(g, new_stone, blinked + 1, new_stones)
      g.add_edge(i, new_stone)
  # endregion
  stones = new_stones

# get the position of each node
pos = nx.get_node_attributes(g, "pos")

# Visualize the graph
if True:
  graph_fig = plt.figure(figsize=(10, 10))
  nx.draw(g, pos=pos, with_labels=True, node_size=1000, font_size=10)
  plt.title("Graph Visualization")
  plt.savefig(here("2024/day11/graph.pdf"))
  plt.show()

# objective: get 22 from this graph
# get roots again from file
roots = list(map(int, Path(file_name).read_text().split(" ")))
ic(roots)


@dataclass
class Out:
  value: int


out = Out(0)
final_stones = []


def transverse(g, root, depth):
  if depth == times_to_blink:
    out.value += 1
    final_stones.append(root)
    return
  for node in g.successors(root):
    transverse(g, node, depth + 1)
  return


for root in roots:
  depth = 0
  transverse(g, root, depth)
print(out.value)
print(final_stones)
