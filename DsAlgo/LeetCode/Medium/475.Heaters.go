package main

import (
	"fmt"
	"sort"
)

func findRadius(houses []int, heaters []int) int {
	sort.Ints(houses)
	sort.Ints(heaters)
	maxRadius := 0

	for _, house := range houses {
		// Binary search to find the closest heater
		idx := sort.SearchInts(heaters, house)
		minDist := 0

		if idx == 0 {
			minDist = abs(heaters[0] - house)
		} else if idx == len(heaters) {
			minDist = abs(house - heaters[len(heaters)-1])
		} else {
			left := abs(house - heaters[idx-1])
			right := abs(heaters[idx] - house)
			if left < right {
				minDist = left
			} else {
				minDist = right
			}
		}

		if minDist > maxRadius {
			maxRadius = minDist
		}
	}

	return maxRadius
}

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func main() {
	houses := []int{1, 2, 3, 4}
	heaters := []int{1, 4}
	fmt.Println(findRadius(houses, heaters)) // Output: 1
}
