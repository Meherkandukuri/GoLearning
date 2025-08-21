package main

func nextPermutation(nums []int) {

	if len(nums) <= 1 {
		return // Handle empty or single-element arrays
	}

	// Step 1: Find the largest index 'k' where nums[k] < nums[k+1]
	k := -1
	for i := len(nums) - 2; i >= 0; i-- {
		if nums[i] < nums[i+1] {
			k = i
			break
		}
	}

	// If no such index, reverse entire array (last permutation)
	if k == -1 {
		reverse(nums, 0)
		return
	}

	// Step 2: Find largest index 'l' > k where nums[k] < nums[l]
	l := len(nums) - 1
	for nums[l] <= nums[k] {
		l--
	}

	// Step 3: Swap elements at k and l
	nums[k], nums[l] = nums[l], nums[k]

	// Step 4: Reverse elements after index k
	reverse(nums, k+1)
}

func reverse(nums []int, start int) {

	if len(nums) == 0 || start < 0 || start >= len(nums) {
		return // Handle invalid inputs gracefully
	}

	end := len(nums) - 1
	for start < end {
		nums[start], nums[end] = nums[end], nums[start]
		start++
		end--
	}
}
