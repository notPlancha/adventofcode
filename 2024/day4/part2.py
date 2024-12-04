with open("input.txt") as f:
  array = [line.strip() for line in f]

count = 0

for i_x in range(1, len(array) - 1):
  for i_y in range(1, len(array[i_x]) - 1):
    if array[i_x][i_y] != "A":
      continue
    if (
       (array[i_x + 1][i_y + 1] == "M" and array[i_x - 1][i_y - 1] == "S"
     or array[i_x + 1][i_y + 1] == "S" and array[i_x - 1][i_y - 1] == "M")
     and
       (array[i_x - 1][i_y + 1] == "M" and array[i_x + 1][i_y - 1] == "S"
     or array[i_x - 1][i_y + 1] == "S" and array[i_x + 1][i_y - 1] == "M")
    ):
      count += 1
    
print(f"{count=}")