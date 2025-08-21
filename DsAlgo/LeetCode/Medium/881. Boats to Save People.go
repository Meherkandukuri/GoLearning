package main

import "sort"

func numRescueBoats(people []int, limit int) int {
	sort.Ints(people)
	left, right := 0, len(people)-1
	count := 0

	for left <= right {
		if people[left]+people[right] <= limit {
			left++
		}
		right--
		count++
	}
	return count
}
