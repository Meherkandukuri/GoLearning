package main

/* 1498. Number of Subsequences That Satisfy the Given Sum Condition
You are given an array of integers nums and an integer target.

Return the number of non-empty subsequences of nums such that the sum of the minimum and maximum element on it is less or equal to target. Since the answer may be too large, return it modulo 109 + 7.
*/

import "sort"

func numSubseq(nums []int, target int) int {

	sort.Ints(nums)
	mod := int(1e9 + 7)
	n := len(nums)

	pow2 := make([]int, n)
	pow2[0] = 1

	for i := 1; i < n; i++ {
		pow2[i] = pow2[i-1] * 2
	}

	res := 0
	left, right := 0, n-1

	for left < right {
		if nums[left]+nums[right] <= target {
			res = (res + pow2[right-left]) % mod
			left++
		} else {
			right--
		}
	}
	return res

}
