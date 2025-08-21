package Medium

import "slices"

func findPairs(nums []int, k int) int {
	if k < 0 || len(nums) == 0 {
		panic("invalid input")
	}

	slices.SortFunc(nums, func(a, b int) int {
		return a - b
	})

	ans := 0
	n := len(nums)
	i := 0

	for i < n-1 {
		if i > 0 && nums[i] == nums[i+1] {
			i++
		}

		for j := i + 1; j < n; j++ {
			diff := nums[j] - nums[i]

			if diff == k {
				ans++
				break
			} else if diff > k {
				break
			}

		}
	}

	return ans

}
