package Medium

func longestMountain(arr []int) int {
	n := len(arr)
	maxLen := 0
	i := 1 // start from the second element

	for i < n-1 {
		// Check if arr[i] is a peak
		if arr[i-1] < arr[i] && arr[i] > arr[i+1] {
			left := i - 1
			right := i + 1

			// Expand left
			for left > 0 && arr[left-1] < arr[left] {
				left--
			}
			// Expand right
			for right < n-1 && arr[right] > arr[right+1] {
				right++
			}

			// Update maxLen
			currLen := right - left + 1
			if currLen > maxLen {
				maxLen = currLen
			}

			// Move i to the end of this mountain
			i = right
		} else {
			i++
		}
	}

	return maxLen
}
