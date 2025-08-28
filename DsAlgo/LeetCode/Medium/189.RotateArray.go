package Medium

import "strings"

func rotate(nums []int, k int) {

	n := len(nums)
	k = k % n

	res := make([]int, n)

	for i := 0; i < n; i++ {
		res[(i+k)%n] = nums[i]
	}

	copy(nums, res)

}
