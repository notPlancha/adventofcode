with open("input.txt") as f:
  array = [line.strip() for line in f]

count = 0

for i_x in range(len(array)):
  for i_y in range(len(array[i_x])):
    if array[i_x][i_y] != "X":
      continue
    # horizontal
    if (
      i_y + 3 < len(array[i_x])
      and array[i_x][i_y + 1] == "M"
      and array[i_x][i_y + 2] == "A"
      and array[i_x][i_y + 3] == "S"
    ): count += 1
    # inverse
    if (
      i_y - 3 >= 0
      and array[i_x][i_y - 1] == "M"
      and array[i_x][i_y - 2] == "A"
      and array[i_x][i_y - 3] == "S"
    ): count += 1
    # vertical down
    if (
      i_x + 3 < len(array)
      and array[i_x + 1][i_y] == "M"
      and array[i_x + 2][i_y] == "A"
      and array[i_x + 3][i_y] == "S"
    ): count += 1
    # vertical up
    if (
      i_x + 3 >= 0
      and array[i_x - 1][i_y] == "M"
      and array[i_x - 2][i_y] == "A"
      and array[i_x - 3][i_y] == "S"
    ): count += 1
    # diagonals
    if(
      i_y + 3 < len(array[i_x]) and i_x + 3 < len(array) 
      and array[i_x + 1][i_y + 1] == "M"
      and array[i_x + 2][i_y + 2] == "A"
      and array[i_x + 3][i_y + 3] == "S"
    ): count += 1
    if(
      i_y - 3 >= 0 and i_x - 3 >= 0
      and array[i_x - 1][i_y - 1] == "M"
      and array[i_x - 2][i_y - 2] == "A"
      and array[i_x - 3][i_y - 3] == "S"
    ): count += 1
    if(
      i_y + 3 < len(array[i_x]) and i_x - 3 >= 0
      and array[i_x - 1][i_y + 1] == "M"
      and array[i_x - 2][i_y + 2] == "A"
      and array[i_x - 3][i_y + 3] == "S"
    ): count += 1
    if(
      i_y - 3 >= 0 and i_x + 3 < len(array)
      and array[i_x + 1][i_y - 1] == "M"
      and array[i_x + 2][i_y - 2] == "A"
      and array[i_x + 3][i_y - 3] == "S"
    ): count += 1
print(f"{count=}")