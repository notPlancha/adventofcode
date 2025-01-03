library(tidyverse)
library(here)
library(icecream)
data <- read_file(here("2024", "day2", "input.txt"))
data %>% str_split("\r\n") -> records
out <- 0

for (record in records[[1]]) {
  levels <- (record %>% str_split(" "))[[1]] %>% as.integer()
  old_lvl <- levels[1]
  decreasing <- (levels[1] > levels[2])
  add_to_out <- T
  for (level in levels[-1]) {
    if (decreasing) {
      if ((old_lvl - level) %>% between(1,3) %>% isFALSE) {
        add_to_out <- F
        break
      }
    } else { # increasing
      if ((level - old_lvl) %>% between(1,3) %>% isFALSE) {
        cat("Old: ", old_lvl, "New: ", level, "Levels" , levels, "\n")
        add_to_out <- F
        break
      }
    }
    old_lvl <- level
  }
  if (add_to_out) {
    out <- out + 1
  }
}
cat("Out: ", out)