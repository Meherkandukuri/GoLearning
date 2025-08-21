package main

func pancakeSort(arr []int) []int {
	n := len(arr)
	res := []int{}

	for currSize := n; currSize > 1; currSize-- {
		// Find index of the maximum element in arr[0:currSize]
		maxIdx := 0
		for i := 1; i < currSize; i++ {
			if arr[i] > arr[maxIdx] {
				maxIdx = i
			}
		}
		// If max is not at its place
		if maxIdx != currSize-1 {
			// Flip max to front if it's not already there
			if maxIdx != 0 {
				reverse969(arr[:maxIdx+1])
				res = append(res, maxIdx+1)
			}
			// Flip max to its correct position
			reverse969(arr[:currSize])
			res = append(res, currSize)
		}
	}
	return res
}

func reverse969(arr []int) {
	start, end := 0, len(arr)-1
	for start < end {
		arr[start], arr[end] = arr[end], arr[start]
		start++
		end--
	}
}
