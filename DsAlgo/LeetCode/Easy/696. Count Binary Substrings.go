package main

import main2 "GoLearning/DsAlgo/LeetCode/Easy/May"

func countBinarySubstrings(s string) int {

	n := len(s)
	prevCount, currentCount := 0, 1
	counter := 0

	for i := 1; i < n; i++ {
		if s[i] == s[i-1] {
			currentCount++
		} else {
			counter += main2.min(prevCount, currentCount)
			prevCount = currentCount
			currentCount += 1
		}
	}

	counter += main2.min(prevCount, currentCount)

	return counter

}
