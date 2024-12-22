from collections import deque, defaultdict
from itertools import pairwise
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from pyprojroot.here import here

import matplotlib.pyplot as plt


def node_on_graph(g, node):
  return node in g


last_of_level: dict[int, int] = defaultdict(lambda: -1)


def add_node(g, node, y_level):
  if node not in g:
    last_of_level[y_level] += 1
    x = last_of_level[y_level]
    g.add_node(node, pos=(x, y_level))
    # add node to the graph at the given y_level and a new x, right to the previous node


file_name = here("2024/day11/test.txt")

g = nx.DiGraph()
stones = deque()
stones.extend(map(int, Path(file_name).read_text().split(" ")))

# region add root stones
for stone in stones:
  add_node(g, stone, 0)

# endregion

# test node_on_graph
print(node_on_graph(g, 17))
assert node_on_graph(g, 17)

for blinked in range(6):
  new_stones = deque()
  # region create new stones and add them to graph and join to previous nodes
  for i in stones:
    if i == 0:
      new_stones.append(1)
      add_node(g, 1, blinked + 1)
      g.add_edge(0, 1)
    elif len(str_i := str(i)) % 2 == 0:
      mid_point = len(str_i) // 2
      new_stones.append(int(str_i[:mid_point]))
      add_node(g, int(str_i[:mid_point]), blinked + 1)
      g.add_edge(i, int(str_i[:mid_point]))
      g.add_edge(i, int(str_i[:mid_point]))
      new_stones.append(int(str_i[mid_point:]))
      add_node(g, int(str_i[mid_point:]), blinked + 1)
      g.add_edge(i, int(str_i[mid_point:]))
    else:
      new_stone = i * 2024
      new_stones.append(new_stone)
      add_node(g, new_stone, blinked + 1)
      g.add_edge(i, new_stone)
  # endregion
  stones = new_stones

# get the position of each node
pos = nx.get_node_attributes(g, "pos")
print(pos)

# Visualize the graph
graph_fig = plt.figure(figsize=(10, 10))
nx.draw(g, pos=pos, with_labels=True, node_size=1000, font_size=10)
plt.title("Graph Visualization")
plt.savefig(here("2024/day11/graph.pdf"))
plt.show()