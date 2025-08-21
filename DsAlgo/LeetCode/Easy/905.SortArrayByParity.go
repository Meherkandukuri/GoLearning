package main

func sortArrayByParity(nums []int) []int {
	n := len(nums)
	res := make([]int, n)
	left, right := 0, n-1

	for i := 0; i < n; i++ {
		if nums[i]%2 == 0 {
			res[left] = nums[i]
			left++
		} else {
			res[right] = nums[i]
			right--
		}
	}

	return res
}
