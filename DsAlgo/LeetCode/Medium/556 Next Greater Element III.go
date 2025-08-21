package main

import "math"

func nextGreaterElement(n int) int {
	var numSlice []int
	num := n
	for num > 0 {
		numSlice = append(numSlice, num%10)
		num = num / 10
	}

	// Reverse the entire slice initially
	reverse(numSlice, 0)

	k := -1
	for i := len(numSlice) - 2; i >= 0; i-- {
		if numSlice[i] < numSlice[i+1] {
			k = i
			break
		}
	}

	if k == -1 {
		return -1
	}

	l := len(numSlice) - 1
	for numSlice[l] <= numSlice[k] {
		l--
	}

	numSlice[k], numSlice[l] = numSlice[l], numSlice[k]

	reverse(numSlice, k+1)

	nextGreaterElement := makeNum(numSlice)

	// Check if the result fits in 32-bit integer
	if nextGreaterElement > math.MaxInt32 {
		return -1
	}

	return nextGreaterElement
}

func makeNum(numSlice []int) int {
	num := 0
	for _, value := range numSlice {
		num = num*10 + value
	}
	return num
}
