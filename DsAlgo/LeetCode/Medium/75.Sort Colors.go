package main

// This is called Dutch National Flag algorithm
func sortColors(nums []int) {

	low, mid, high := 0, 0, len(nums)-1

	switch nums[mid] {
	case 0:
		nums[low], nums[mid] = nums[mid], nums[low]
		mid++
		low++

	case 1:
		mid++

	case 2:
		nums[mid], nums[high] = nums[high], nums[mid]
		high--
	}

}
