package main

func getNextIndex(nums []int, direction bool, pointer int) int {
	currDirec := nums[pointer] > 0
	if currDirec != direction {
		return -1
	}
	n := len(nums)
	nextIndex := (pointer + nums[pointer]) % n
	if nextIndex < 0 {
		nextIndex += n
	}
	if nextIndex == pointer {
		return -1
	}
	return nextIndex
}

func circularArrayLoop(nums []int) bool {
	hm := map[int]bool{}
	for i := 0; i < len(nums); i++ {
		if hm[i] {
			continue
		}
		direction := nums[i] > 0
		slow, fast := i, i
		for {
			slow = getNextIndex(nums, direction, slow)
			fast = getNextIndex(nums, direction, fast)
			if fast != -1 {
				fast = getNextIndex(nums, direction, fast)
			}
			if slow == -1 || fast == -1 || slow == fast {
				break
			}
			hm[slow] = true
			hm[fast] = true
		}
		if slow != -1 && fast != -1 && slow == fast {
			return true
		}
	}
	return false
}
