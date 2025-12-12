from dataclasses import dataclass
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


def click_buttons_from_counts(machine: Machine, buttons_counts: list[tuple[int, Button]]) -> Machine:
  new_m = machine.copy()
  for count, button in buttons_counts:
    for _ in range(count):
      new_m.click_button(button)
  return new_m
  
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
      - get index of min of objective
      - find buttons that click that index
      - make combinations of those buttons (with sum of counter = min)
      - 1 state per combination
      - check if state is objective
      - if not check if any index exceeds objective, if so discard
      - discard buttons that click that index
      - repeat
  """
  machine_list = [machine]
  indexes_checked = set()
  buttons_checked = set()
  for _ in range(sum(machine.objective)):
    # get index of min
    tmp = [999 if i in indexes_checked else machine.objective[i] for i in range(len(machine.objective))]
    index_of_min = tmp.index(min_obj := min(tmp))
    # find buttons that click that index
    buttons_that_click_min = [
      button for button in machine.buttons if index_of_min in button
    ]
    buttons_that_click_min = [b for b in buttons_that_click_min if b not in buttons_checked]
    ic(index_of_min, min_obj, buttons_that_click_min, [machine.state for machine in machine_list])
    new_machine_list = []
    # Discard Buttons and index that is going to be used
    for b in buttons_that_click_min:
      buttons_checked.add(b)
    indexes_checked.add(index_of_min)
    
    ic(indexes_checked, buttons_checked)
    if len(buttons_that_click_min) == 0:
      continue
    
    # make combinations of those buttons
    for machine_ in machine_list:
      for tup in distribute(min_obj - machine_.state[index_of_min], len(buttons_that_click_min)): # tup is (0,0,7)
        new_m = click_buttons_from_counts(
          machine_.copy(),
          [(tup[i], buttons_that_click_min[i]) for i in range(len(buttons_that_click_min))]
        )
        new_machine_list.append(new_m)
    machine_list = new_machine_list
    # check here
    rets = []
    for m in machine_list:
      if check(m):
        rets.append(m)
    if len(rets) > 0:
      ic(rets)
      return min(
        sum(m.button_click_count.values()) for m in rets
      )
    
    # DONT FILTER BECAUSE IT CAN FUCK UP INDEXES OF BUTTONS I CACHING THEM
    pass
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
  ic.disable()
  for machine in machines:
    ic(machine.objective)
    ret += ic(find_in_machine(machine=machine))
    print(f"{machine.objective=},{ret=}")
  print(ret)

