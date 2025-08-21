package Medium

func maxArea(height []int) int {
	maxWater := 0
	left, right := 0, len(height)-1

	for left < right {

		currentHeight := min(height[left], height[right])
		width := right - left
		maxWater = max(maxWater, currentHeight*width)

		if height[left] < height[right] {
			left++
		} else {
			right--
		}
	}
	return maxWater
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
