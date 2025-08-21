package main

import "sort"

/*
923. 3Sum With Multiplicity
Given an integer array arr, and an integer target, return the number of tuples i, j, k such that i < j < k and arr[i] + arr[j] + arr[k] == target.
As the answer can be very large, return it modulo 109 + 7.
*/

func threeSumMulti(arr []int, target int) int {
	var trippletCount int
	var sum int
	sort.Ints(arr)
	n := len(arr)
	mod := int(1e9 + 7)

	for i := 0; i <= n-2; i++ {
		remaining := target - arr[i]

		left, right := i+1, n-1

		for left < right {
			sum = arr[left] + arr[right]

			if sum < remaining {
				left++
			} else if sum > remaining {
				right--
			} else {
				// Count duplicates at left and right positions
				if arr[left] == arr[right] {
					// If all elements between left and right are the same
					count := right - left + 1
					// Number of ways to choose 2 elements from count elements
					trippletCount = (trippletCount + count*(count-1)/2) % mod
					break
				} else {
					rightCount, leftCount := 1, 1
					for left+1 < right && arr[left] == arr[left+1] {
						leftCount++
						left++
					}

					for right-1 > left && arr[right] == arr[right-1] {
						rightCount++
						right--
					}
					trippletCount = (trippletCount + (leftCount * rightCount)) % mod

					left++
					right--
				}
			}

		}

	}
	return trippletCount

}
