from collections import deque
from itertools import pairwise
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from pyprojroot.here import here

def node_on_graph(g, node):
  return str(node) in g


file_name = here("2024/day11/test.txt")

g = nx.DiGraph()
stones = deque()
stones.extend(map(int, Path(file_name).read_text().split(" ")))

# region add root stones
for stone in stones:
  g.add_node(str(stone))
  # with g.subgraph() as s:
  #   s.graph["rank"] = "min"
  #   s.add_node(str(stone))
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
      g.add_node("1")
      g.add_edge("0", "1")
    elif len(str_i := str(i)) % 2 == 0:
      mid_point = len(str_i) // 2
      new_stones.append(int(str_i[:mid_point]))
      g.add_node(str(int(str_i[:mid_point])))
      g.add_edge(str(i), str(int(str_i[:mid_point])))
      g.add_edge(str(i), str(int(str_i[:mid_point])))
      new_stones.append(int(str_i[mid_point:]))
      g.add_node(str(int(str_i[mid_point:])))
      g.add_edge(str(i), str(int(str_i[mid_point:])))
    else:
      new_stone = i * 2024
      new_stones.append(new_stone)
      g.add_node(f"{new_stone}")
      g.add_edge(f"{i}", f"{new_stone}")
  # endregion
  # region add newly created nodes as same rank
  # with g.subgraph() as s:
  #   s.graph["rank"] = "same"
  #   for stone in new_stones:
  #     if not node_on_graph(g, stone):
  #       s.add_node(f"{stone}")
  # endregion
  stones = new_stones

# region define root nodes as rank min
for stone in stones:
  g.add_node(stone)
  # with g.subgraph() as s:
  #   s.graph["rank"] = "min"
  #   s.add_node(stone)
# endregion
import matplotlib.pyplot as plt

# Visualize the graph
graph_layout = nx.nx_agraph.graphviz_layout(g, prog="dot")
graph_fig = plt.figure(figsize=(10, 10))
nx.draw(g, pos=graph_layout, with_labels=True, node_size=1000, font_size=10)
plt.title("Graph Visualization")
plt.savefig(here("2024/day11/graph.pdf"))
plt.close()
