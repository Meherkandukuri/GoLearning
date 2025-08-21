package main

func removeDuplicates(nums []int) int {

	idx := 0
	n := len(nums)
	i := 0

	for i < n {
		num := nums[i]
		for i < n && nums[i] == num {
			i++
		}

		nums[idx] = num
		idx++
	}

	return idx
}
