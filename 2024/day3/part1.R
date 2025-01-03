library(tidyverse)
library(here)
library(magrittr)

memory <- read_file(here("2024", "day3", "input.txt"))
regex <- r"{mul\((\d+),(\d+)\)}"
numbers <- str_match_all(memory, regex) %>% .[[1]] %>% as_tibble
numbers %<>% mutate(result = as.numeric(V2)*as.numeric(V3)) 
cat("out:", numbers["result"] %>% sum)