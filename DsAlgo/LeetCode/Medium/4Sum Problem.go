package Medium

import "sort"

/*


Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:

0 <= a, b, c, d < n
a, b, c, and d are distinct.
nums[a] + nums[b] + nums[c] + nums[d] == target
You may return the answer in any order.
*/

func fourSum(nums []int, target int) [][]int {
	var result [][]int
	n := len(nums)

	// Handle edge cases
	if n < 4 {
		return result
	}

	// Sort the array
	sort.Ints(nums)

	// Use early termination and bounds checking
	for i := 0; i < n-3; i++ {
		// Skip duplicates
		if i > 0 && nums[i] == nums[i-1] {
			continue
		}

		// Early termination checks
		// If smallest possible sum > target, no need to continue
		if nums[i]+nums[i+1]+nums[i+2]+nums[i+3] > target {
			break
		}

		// If largest possible sum < target, skip this i
		if nums[i]+nums[n-3]+nums[n-2]+nums[n-1] < target {
			continue
		}

		for j := i + 1; j < n-2; j++ {
			// Skip duplicates
			if j > i+1 && nums[j] == nums[j-1] {
				continue
			}

			// Early termination checks for j
			// If smallest possible sum > target, no need to continue with this j
			if nums[i]+nums[j]+nums[j+1]+nums[j+2] > target {
				break
			}

			// If largest possible sum < target, skip this j
			if nums[i]+nums[j]+nums[n-2]+nums[n-1] < target {
				continue
			}

			left, right := j+1, n-1

			for left < right {
				sum := nums[i] + nums[j] + nums[left] + nums[right]

				if sum < target {
					left++
				} else if sum > target {
					right--
				} else {
					// Found a quadruplet
					result = append(result, []int{nums[i], nums[j], nums[left], nums[right]})

					// Skip duplicates
					for left < right && nums[left] == nums[left+1] {
						left++
					}
					for left < right && nums[right] == nums[right-1] {
						right--
					}

					left++
					right--
				}
			}
		}
	}

	return result
}
