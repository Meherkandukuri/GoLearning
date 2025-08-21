package main

import "math"

/*
PROBLEM STATEMENT
633. Sum of Square Numbers
Given a non-negative integer c, decide whether there're two integers a and b such that a2 + b2 = c.
*/

func judgeSquareSum(c int) bool {

	left, right := 0, int(math.Sqrt(float64(c)))
	var sum int
	for left <= right {
		sum = left*left + right*right
		if sum == c {
			return true
		} else if sum < c {
			left++
		} else {
			right--
		}
	}
	return false
}
