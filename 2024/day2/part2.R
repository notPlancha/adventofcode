library(tidyverse)
library(here)
library(icecream)
data <- read_file(here("2024", "day2", "input.txt"))
data %>% str_split("\r\n") -> records
out <- 0

isCorrect <- \(vec) {
  decreasing <- (vec[1] > vec[2])
  old_lvl <- vec[1]
  for (i in 2:length(vec)) {
    level <- vec[i]
    if (decreasing) {
      if ((old_lvl - level) %>% between(1,3) %>% isFALSE) {
        return(F)
      }
    } else {
      if ((level - old_lvl) %>% between(1,3) %>% isFALSE) {
        return(F)
      }
    }
    old_lvl <- level
  }
  return(T)
}
for (record in records[[1]]) {
  levels <- (record %>% str_split(" "))[[1]] %>% as.integer()
  if (isCorrect(levels)) {
    out <- out + 1
  } else {
    for (level_to_rem in 1:length(levels)) {
      if(isCorrect(levels[-level_to_rem])) {
        out <- out + 1
        break
      }
    }
  }
}
cat("Out: ", out)