package main

import "math"

func sortedSquares(nums []int) []int {

	n := len(nums)
	res := make([]int, n)
	left, right := 0, n-1

	for i := len(nums) - 1; i >= 0; i-- {
		if math.Abs(float64(nums[left])) > math.Abs(float64(nums[right])) {
			res[i] = nums[left] * nums[left]
			left++
		} else {
			res[i] = nums[right] * nums[right]
			right--
		}
	}

	return res
}
