import timeit
import math

# Loop-based method
def num_digits_loop(number):
  count = 0
  while number > 0:
    number //= 10
    count += 1
  return count

# String-based method
def num_digits_string(number):
  return len(str(number))

# Logarithmic method
def num_digits_log(number):
  return math.floor(math.log10(number)) + 1 if number > 0 else 1

# Test number
large_number = 12345678901234567890

# Benchmarking
loop_time = timeit.timeit(lambda: num_digits_loop(large_number), number=100000)
string_time = timeit.timeit(lambda: num_digits_string(large_number), number=100000)
log_time = timeit.timeit(lambda: num_digits_log(large_number), number=100000)

# Results
print(f"Loop-Based Method Time: {loop_time:.6f} seconds")
print(f"String-Based Method Time: {string_time:.6f} seconds")
print(f"Logarithmic Method Time: {log_time:.6f} seconds")
# Original mathematical method
def split_integer(number):
  temp = number
  num_digits = 0
  while temp > 0:
    temp //= 10
    num_digits += 1
  power_of_ten = 10 ** (num_digits // 2)
  return number // power_of_ten, number % power_of_ten


# String-based method
def split_integer_with_string(number):
  num_str = str(number)
  mid_point = len(num_str) // 2
  return int(num_str[:mid_point]), int(num_str[mid_point:])


# Optimized mathematical method
def split_integer_optimized(number):
  power_of_ten = 10 ** ((math.floor(math.log10(number)) + 1) // 2)
  return number // power_of_ten, number % power_of_ten


# Test number
large_number = 12345678901234567890

# Benchmarking
non_string_time = timeit.timeit(lambda: split_integer(large_number), number=100000)
string_time = timeit.timeit(lambda: split_integer_with_string(large_number), number=100000)
optimized_time = timeit.timeit(lambda: split_integer_optimized(large_number), number=100000)

# Results
print(f"Original Mathematical Method Time: {non_string_time:.6f} seconds")
print(f"String-Based Method Time: {string_time:.6f} seconds")
print(f"Optimized Mathematical Method Time: {optimized_time:.6f} seconds")
