from collections import deque, defaultdict
from itertools import chain

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
  roots = stones = deque()
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

  #region color nodes without edges
  # nodes_without_edges = [n for n, d in list(g.out_degree) if d == 0]
  # for node in nodes_without_edges:
  #   g.nodes[node]["color"] = "green"
  #endregion

  # region Visualize the graph
  def plot_graph(file_name = here("2024/day11/graph.pdf")):
    pos = nx.get_node_attributes(g, "pos")
    plt.figure(figsize=(10, 10))
    # find out colors
    colors = [g.nodes[n].get("color", "skyblue") for n in g.nodes]
    nx.draw(g, pos=pos, with_labels=True, node_size=1000, font_size=10, node_color=colors, edge_color="gray")
    plt.title("Graph Visualization")
    plt.savefig(here("2024/day11/graph.pdf"))
    plt.show()
  if viz:
    plot_graph()
  #endregion

  #region loop fast slow
  def advance_slow(root: int):
    yielded = deque()
    yielded.append(root)
    while True:
      yield yielded
      to_yield = deque()
      for node in yielded:
        to_yield.extend(g.successors(node))
      yielded = to_yield

  def advance_fast(root: int):
    yielded = deque()
    yielded.append(root)
    should_yield = True
    while True:
      if should_yield: yield yielded
      to_yield = deque()
      for node in yielded:
        to_yield.extend(g.successors(node))
      yielded = to_yield
      should_yield = False if should_yield is True else True


  for root in roots:
    slow_iter = iter(advance_slow(root))
    fast_iter = iter(advance_fast(root))
    for i in range(25):
      slows = next(slow_iter)
      fasts = next(fast_iter)
      # plot graph with slows and fast colored
      for slow in slows:
        g.nodes[slow]["color"] = "yellow"
      for fast in fasts:
        g.nodes[fast]["color"] = "lightgreen"
      # color conincident nodes
      for coincident in set(slows).intersection(fasts):
        g.nodes[coincident]["color"] = "purple"
      plot_graph()
      # reset colors
      for slow in slows:
        g.nodes[slow]["color"] = "skyblue"
      for fast in fasts:
        g.nodes[fast]["color"] = "skyblue"
    break  # temp
#endregion



if __name__ == '__main__':
  main(viz=True, file_name=here("2024/day11/test.txt"), times_to_blink=75)
