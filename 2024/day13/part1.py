from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from dataclasses import dataclass

with open('grammar.ppeg') as file:
  grammar = Grammar(file.read())
with open("input.txt") as file:
  parsed = grammar.parse(file.read())


@dataclass
class Machine:
  a_x: int
  a_y: int
  b_x: int
  b_y: int
  prize_x: int
  prize_y: int


# Create a visitor to process the parse tree and extract the data
class ExtractNumbersVisitor(NodeVisitor):
  def visit_data(self, node):
    # Process the entry nodes to extract button data
    entries = [self.visit(entry) for entry in node.children]
    return entries

  def visit_entry(self, node):
    # Each entry contains two buttons and a prize
    button_a, coords_a, _, button_b, coords_b, _, prize, *_ = node.children
    coords_a_values = self.visit(coords_a)
    coords_b_values = self.visit(coords_b)
    prize_values = self.visit(prize)

    # Create a Machine object with the extracted values
    return Machine(
      a_x=coords_a_values[0],
      a_y=coords_a_values[1],
      b_x=coords_b_values[0],
      b_y=coords_b_values[1],
      prize_x=prize_values[0],
      prize_y=prize_values[1]
    )

  def visit_button(self, node):
    # Extract the button label (A or B) from the "Button X:" pattern
    return node.children[1].text  # This will return "A" or "B"

  def visit_coords(self, node):
    # Extract the coordinates from the "X+<number>, Y+<number>" pattern
    x_value = int(node.children[0].text[2:])  # Skipping 'X+'
    y_value = int(node.children[2].text[2:])  # Skipping 'Y+'
    return (x_value, y_value)

  def visit_prize(self, node):
    # Extract the prize coordinates from the "Prize: X=<number>, Y=<number>" pattern
    x_value = int(node.children[2].text)
    y_value = int(node.children[4].text)
    return (x_value, y_value)



visitor = ExtractNumbersVisitor()
extracted_data = visitor.visit(parsed)

# Print extracted data as Machine instances
for machine in extracted_data:
  print(machine)
