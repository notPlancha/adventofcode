from dataclasses import dataclass
import itertools
import more_itertools
from icecream import ic
from collections import Counter
machines = []

type Joltage_level = int
type Index = int
type Button = tuple[Index, ...]


@dataclass
class Machine:
  state: list[Joltage_level]
  objective: list[Joltage_level]
  buttons: list[Button]
  _initial_state: list[Joltage_level]
  button_click_count: Counter
  
  def reset_state(self):
    self.state = self._initial_state.copy()
  
  def click_button(self, button: Button):
    self.button_click_count[button] += 1
    for b in button:
      self.state[b] += 1    

  def copy(self) -> "Machine":
    return Machine(
      state = self.state.copy(),
      objective = self.objective,
      buttons = self.buttons.copy(),
      _initial_state = self._initial_state,
      button_click_count = self.button_click_count.copy()
    )

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
      _initial_state = [0 for _ in joltage.split(",")],
      button_click_count = Counter()
    ))
    
def check(machine) -> bool:
  return machine.state == machine.objective

def find_in_machine(machine: Machine) -> int:
  """
    heuristic approach:
      - get index of max of objective
      - find buttons that click that index
      - make combinations of those buttons (with sum of counter = max)
      - 1 state per combination
      - check if state is objective
      - if not check if any index exceeds objective, if so discard
      - discard buttons that click that index
      - repeat
  """
  machine_list = [machine]
  for _ in range(sum(machine.objective)):
    # get index of max
    index_of_max = machine.objective.index(max_obj := max(machine.objective))
    # find buttons that click that index
    buttons_that_click_max = [
      button for button in machine.buttons if index_of_max in button
    ]
    # make combinations of those buttons
    new_machine_list = []
    for machine_ in machine_list:
      new_m = machine_.copy()
      for tup in distribute(max_obj, len(buttons_that_click_max)): # tup is (7,0,0)
        for i, count in enumerate(tup):
          for _ in range(count):
            new_m.click_button(buttons_that_click_max[i])
      if check(new_m):
        return sum(new_m.button_click_count.values())
      new_machine_list.append(new_m)
    machine_list = new_machine_list
    # filter out machines that exceed objective
    machine_list = [
      m for m in machine_list if all(
        m.state[i] <= m.objective[i] for i in range(len(m.state))
      )
    ]
    # discard buttons that click that index
    for m in machine_list:
      m.buttons = [
        button for button in m.buttons if index_of_max not in button
      ]
    # repeat
  raise Exception(f"No solution found: {machine.objective}")
        
def distribute(n, k):
  if k == 1:
    yield (n,)
    return
  for i in range(n + 1):
    for tail in distribute(n - i, k - 1):
      yield (i,) + tail


if __name__ == "__main__":
  ret = 0
  # ic.disable()
  for machine in machines:
    ic(machine.objective)
    ret += find_in_machine(machine=machine)
  print(ret)

