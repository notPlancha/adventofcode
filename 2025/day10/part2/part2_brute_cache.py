from dataclasses import dataclass
import itertools
import more_itertools
from icecream import ic
from functools import cache

machines = []

type Joltage_level = int
type Index = int
type Button = tuple[Index, ...]
type Count = int
type Counts = tuple[Count, ...]
@dataclass
class Machine:
  state: list[Joltage_level]
  objective: list[Joltage_level]
  buttons: list[Button]
  _initial_state: list[Joltage_level]
  
  def reset_state(self):
    self.state = self._initial_state.copy()


def click_button(state: list[Joltage_level], button: Button) -> list[Joltage_level]:
  state = state.copy()
  for index in button:
    state[index] += 1
  return state

def click_buttons_from_counts(state: list[Joltage_level], buttons: list[Button], counts: Counts) -> list[Joltage_level]:
  state = state.copy()
  for i in range(len(buttons)):
    for _ in range(counts[i]):
      state = click_button(state, buttons[i])
  return state

# read file
with open("2025/day10/input.txt") as f:
  lines = f.readlines()
  for line in lines:
    parts = line.split(" ")
    joltage : str = parts[-1].strip()[1:-1]
    buttons: list[str] = [part[1:-1] for part in parts[1:-1]]
    machines.append(Machine(
      objective = [int(c) for c in joltage.split(",")],
      state = [0 for _ in joltage.split(",")],
      buttons = [tuple(int(x) for x in button.split(",")) for button in buttons],
      _initial_state = [0 for _ in joltage.split(",")]
    ))
    
def check(machine: Machine) -> bool:
  return machine.state == machine.objective

def find_in_machine(machine: Machine) -> int:
  checked_comb: set[Counts] = set()
  depth = 0
  current_depth_counts: list[Counts] = [tuple(0 for _ in machine.buttons)]
  
  def build_next_depth(current_depth) -> list[Counts]:
    new_counts = []
    for counts in current_depth:
      counts_l = list(counts)
      for i in range(len(counts_l)):
        counts_l[i] += 1
        if (counts_t := tuple(counts_l)) not in checked_comb:
          checked_comb.add(counts_t)
          new_counts.append(counts_t)
        counts_l[i] -= 1
    return new_counts
  
  for _ in range(500):
    for counts in current_depth_counts:
      if (click_buttons_from_counts(machine._initial_state, machine.buttons, counts) == machine.objective):
        ic(counts, depth)
        return depth
    depth += 1
    current_depth_counts = build_next_depth(current_depth_counts)
  raise Exception(f"Not found: {machine.objective}")
from time import perf_counter
if __name__ == "__main__":
  start = perf_counter()
  ret = 0
  ic.disable()
  for machine in machines:
    ic(machine.objective)
    ret += find_in_machine(machine=machine)
  end = perf_counter()
  print(f"Time taken: {end - start} seconds")
  print(ret)
