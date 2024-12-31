package main

import (
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

func Importdata() ([]int, []int) {

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
	col1, col2 := Importdata()
	slices.Sort(col1)
	slices.Sort(col2)
	diff := make([]int, 0, len(col1))
	for i := range col1 {
		diff = append(diff, abs(col1[i]-col2[i]))
	}
	println(sum(diff))
}

func sum(array []int) int {
	result := int(0)
	for _, v := range array {
		result += v
	}
	return result
}

func abs(n int) int {
	if n > 0 {
		return n
	} else {
		return -n
	}
}
