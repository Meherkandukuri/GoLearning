package main

func sortArrayByParityII(nums []int) []int {
	even, odd := 0, 1
	n := len(nums)
	for even < n && odd < n {
		if nums[even]%2 == 0 {
			even += 2
		} else if nums[odd]%2 == 1 {
			odd += 2
		} else {
			nums[even], nums[odd] = nums[odd], nums[even]
			even += 2
			odd += 2
		}
	}
	return nums
}
