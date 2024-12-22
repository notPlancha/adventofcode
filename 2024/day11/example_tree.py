from collections import deque
from itertools import pairwise
from pathlib import Path

import graphviz
from graphviz import Digraph


def node_on_graph(g, node):
  return f'\t{node}\n' in g.body
file_name = "test.txt"

g = Digraph("stones", strict=True)
stones = deque()
stones.extend(map(int, Path(file_name).read_text().split(" ")))
#region add root stones
for stone in stones:
  g.node(str(stone))
  with g.subgraph() as s:
    s.attr(rank="min")
    s.node(str(stone))
#endregion

# test node_on_graph
print(node_on_graph(g, 17))
print(g.body)
assert node_on_graph(g, 17)

for blinked in range(6):
  new_stones = deque()
  #region create new stones and add them to graph and join to previous ndoes
  for i in stones:
    if i == 0:
      new_stones.append(1)
      g.node("1")
      g.edge("0", "1")
    elif len(str_i := str(i)) % 2 == 0:
      mid_point = len(str_i) // 2
      new_stones.append(int(str_i[:mid_point]))
      g.node(str(int(str_i[:mid_point])))
      g.edge(str(i), str(int(str_i[:mid_point])))
      g.edge(str(i), str(int(str_i[:mid_point])))
      new_stones.append(int(str_i[mid_point:]))
      g.node(str(int(str_i[mid_point:])))
      g.edge(str(i), str(int(str_i[mid_point:])))
    else:
      new_stone = i * 2024
      new_stones.append(new_stone)
      g.node(f"{new_stone}")
      g.edge(f"{i}", f"{new_stone}")
  #endregion
  #region add newly created nodes as same rank
  with g.subgraph() as s:
    s.attr(rank="same")
    for stone in new_stones:
      if not node_on_graph(g, stone):
        s.node(f"{stone}")
  #endregion
  stones = new_stones

#region define root nodes as rank min
stones = deque()
stones.extend(Path(file_name).read_text().split(" "))
for stone in stones:
  g.node(stone)
  with g.subgraph() as s:
    s.attr(rank="min")
    s.node(stone)
#endregion
import networkx as nx
from networkx.drawing.nx_agraph import from_agraph

gg = from_agraph(g, create_using=nx.DiGraph())

g.render("graph", view=True)
