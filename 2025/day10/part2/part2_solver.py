"""
e.g.: (3,4,5,6,7) (1,3,4,5,6,8) (0,1,2,3,4,6,8) (1,2,7) (2,3,4,6,8) (2,5,6,7,8) (0,2,4,5,6,8) (1,2,3,5,6,7,8) {35,149,194,51,68,54,85,164,67}
Do a matrix
0 1 2 3 4 5 6 7 8
-----------------
0 0 0 x x x x x 0
0 y 0 y y y y 0 y
z z z z z 0 z 0 z
etc

then solve:
minimize: x + y + z + ...
subject to:
0 + 0 + z + ... = 35
0 + y + z + ... = 149
x + 0 + z + ... = 194
"""
import pyomo.environ as pyo
from dataclasses import dataclass
from icecream import ic

@dataclass
class Problem:
  joltages: list[int]
  buttons: list[tuple[int, ...]]

problem_list = []
with open("2025/day10/input.txt") as f:
  lines = f.readlines()
  for line in lines:
    joltages = line.split(" ")[-1].strip()[1:-1]
    joltages_list: list[int] = [int(c) for c in joltages.split(",")]
    buttons: list[tuple[int, ...]] = [tuple(int(x) for x in part[1:-1].split(",")) for part in line.split(" ")[1:-1]]
    problem_list.append(Problem(
      joltages = joltages_list,
      buttons = buttons
    ))

def construct_model(problem: Problem) -> pyo.ConcreteModel:
  model: pyo.ConcreteModel = pyo.ConcreteModel()
  
  # n_constraints = n_joltages
  # n_vars = n_buttons
  
  # vars
  model.x = pyo.Var(range(len(problem.buttons)), domain=pyo.NonNegativeIntegers)
  
  # obj
  
  expr = 0
  for i in range(len(problem.buttons)):
    expr += model.x[i]
  
  model.OBJ = pyo.Objective(expr = expr, sense =pyo.minimize)
  
  
  # constrains
  # build constrains matrix ( rows = joltages, cols = buttons)
  matrix: list[list[int | pyo.Var]] = []
  for jolt_pos in range(len(problem.joltages)):
    line = []
    for button_ind in range(len(problem.buttons)):
      if jolt_pos in problem.buttons[button_ind]:
        line.append(model.x[button_ind])
      else:
        line.append(0)
    matrix.append(line)
  
  assert len(matrix) == len(problem.joltages)
  
  # apply constrains matrix horizontally
  for i, line in enumerate(matrix):
    setattr(model, f"Constraint_{problem.joltages[i]}_{i}", pyo.Constraint(expr = pyo.quicksum(line) == problem.joltages[i]))
  
  return model

def transpose(matrix):
    if not matrix:
        return []
    # Ensure all rows have equal length or raise a clear error
    row_length = len(matrix[0])
    if any(len(row) != row_length for row in matrix):
        raise ValueError("All rows must have the same length to transpose.")

    return [list(col) for col in zip(*matrix)]


if __name__ == "__main__":
  ret = 0
  import cplex
  solver = pyo.SolverFactory('cplex_direct')
  # solver.available(exception_flag=True)
  for problem in problem_list:
    model = construct_model(problem)
    # model.pprint()
    solver.solve(model)
    total_clicks = pyo.value(model.OBJ)
    ret += total_clicks
    print(f"{problem.joltages=}, {total_clicks=}")
  print(f"Total: {ret}")