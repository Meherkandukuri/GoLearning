package main

import "sort"

func minPairSum(nums []int) int {
	sort.Ints(nums)
	left, right := 0, len(nums)-1
	var maxSum int
	var currSum int

	for left <= right {
		currSum = nums[left] + nums[right]
		if maxSum < currSum {
			maxSum = currSum
		}
		left++
		right--
	}
	return maxSum
}
