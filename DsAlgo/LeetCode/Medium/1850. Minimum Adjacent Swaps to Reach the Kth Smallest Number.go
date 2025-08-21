package main

import "strconv"

func getMinSwaps(num string, k int) int {
	// Convert string to slice of digits
	original := convstringToSliceOfDigits(num)
	target := make([]int, len(original))
	copy(target, original)

	// Find the kth permutation
	for i := 0; i < k; i++ {
		target = nextPermutationlocal(target)
	}

	// Count the number of swaps
	return countSwaps(original, target)
}

func convstringToSliceOfDigits(number string) []int {
	digitsSlice := make([]int, len(number))
	for i, char := range number {
		digitsSlice[i], _ = strconv.Atoi(string(char))
	}
	return digitsSlice
}

func nextPermutationlocal(nums []int) []int {

	if len(nums) <= 1 {
		return nums // Handle empty or single-element arrays
	}

	i := len(nums) - 2
	for i >= 0 && nums[i] >= nums[i+1] {
		i--
	}
	if i >= 0 {
		j := len(nums) - 1
		for j >= 0 && nums[j] <= nums[i] {
			j--
		}
		nums[i], nums[j] = nums[j], nums[i]
	}
	reverse(nums, i+1)
	return nums
}

func countSwaps(original, target []int) int {
	swaps := 0
	for i := 0; i < len(original); i++ {
		j := i
		for j < len(original) && original[j] != target[i] {
			j++
		}
		for j > i {
			original[j], original[j-1] = original[j-1], original[j]
			j--
			swaps++
		}
	}
	return swaps
}
