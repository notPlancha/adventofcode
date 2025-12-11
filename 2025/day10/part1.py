from dataclasses import dataclass
import itertools
import more_itertools
from icecream import ic

machines = []

@dataclass
class Machine:
  state: list[bool]
  objective: list[bool]
  buttons: list[set[int]]
  _initial_state: list[bool]
  
  def reset_state(self):
    self.state = self._initial_state.copy()


def click_button(state: list[bool], button: set[int]):
  state = state.copy()
  for b in button:
    state[b] = False if state[b] else True
  return state

# read file
with open("2025/day10/input.txt") as f:
  lines = f.readlines()
  for line in lines:
    parts = line.split(" ")
    machines.append(Machine(
      objective = [c == "#" for c in parts[0][1:-1].strip()],
      state = [False for _ in parts[0].strip()],
      buttons = [set(int(x) for x in part[1:-1].split(",")) for part in parts[1:-1]],
      _initial_state = [False for _ in parts[0][1:-1].strip()]
    ))

def check(machine: Machine) -> bool:
  return machine.state == machine.objective

def find_in_machine(machine: Machine) -> int:
  for buttons_comb in more_itertools.powerset(machine.buttons):
    ic(buttons_comb)
    machine.reset_state()
    for button in buttons_comb:
      machine.state = click_button(machine.state, button)
      ic(machine.state)
    if check(machine):
      return len(buttons_comb)
  raise Exception(f"No solution found: {machine.objective}")

if __name__ == "__main__":
  ret = 0
  # disable ic
  ic.disable()
  for machine in machines:
    ic(machine.objective)
    ret += find_in_machine(machine=machine)
  print(ret)