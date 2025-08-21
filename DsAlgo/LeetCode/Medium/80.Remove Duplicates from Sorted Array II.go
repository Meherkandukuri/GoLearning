package Medium

func removeDuplicates80(nums []int) int {
	k := 0
	for i := 0; i < len(nums); i++ {
		// Always keep the first two elements, or if current is not equal to nums[k-2]
		if k < 2 || nums[i] != nums[k-2] {
			nums[k] = nums[i]
			k++
		}
	}
	return k
}
