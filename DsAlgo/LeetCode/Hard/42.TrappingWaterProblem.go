package main

func trap(height []int) int {
	if len(height) == 0 {
		return 0
	}

	waterCount := 0
	left, right := 0, len(height)-1
	maxLeft, maxRight := height[left], height[right]

	for left < right {
		if maxLeft <= maxRight {
			left++
			if maxLeft < height[left] {
				maxLeft = height[left]
			}
			waterCount += maxLeft - height[left]
		} else {
			right--
			if maxRight < height[right] {
				maxRight = height[right]
			}
			waterCount += maxRight - height[right]
		}
	}

	return waterCount
}
