library(tidyverse)
library(here)
library(magrittr)
library(icecream)

memory <- read_file(here("2024", "day3", "input.txt"))
regex_to_rem <- r"{don't\(\).*?(do\(\)|$)}"
memory %<>% str_remove_all("[\r\n]") %>% str_remove_all(regex_to_rem)


regex <- r"{mul\((\d+),(\d+)\)}"
numbers <- str_match_all(memory, regex) %>% .[[1]] %>% as_tibble
numbers %<>% mutate(result = as.numeric(V2)*as.numeric(V3)) 
cat("out:", numbers["result"] %>% sum)