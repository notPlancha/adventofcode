package main

import (
	"log"
	"os"
	"strconv"
	"strings"
)

func importdata() ([]int, []int) {

	//region data
	currentDir, _ := os.Getwd()
	data, err := os.ReadFile(currentDir + "/2024/day1/input.txt")
	if err != nil {
		log.Fatal(err)
	}

	// Split the columns into 2 arrays
	lines := strings.Split(string(data), "\n")
	col1 := make([]int, 0, len(lines))
	col2 := make([]int, 0, len(lines))

	for _, line := range lines {
		if line == "" {
			continue
		}
		columns := strings.Fields(line) // Adjust delimiter if needed
		num1, _ := strconv.Atoi(columns[0])
		num2, _ := strconv.Atoi(columns[1])
		col1 = append(col1, num1)
		col2 = append(col2, num2)
	}
	//endregion
	return col1, col2
}

func main() {
	col1, col2 := importdata()

	counter := make(map[int]int)
	for _, n := range col2 {
		if _, ok := counter[n]; ok {
			counter[n] += 1
		} else {
			counter[n] = 1
		}
	}
	out := 0
	for _, n := range col1 {
		if _, ok := counter[n]; ok {
			out += n * counter[n]
		}
	}
	println(out)
}
