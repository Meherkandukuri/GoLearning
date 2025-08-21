package Medium

func numSubarrayBoundedMax(A []int, L int, R int) int {
	if len(A) == 0 {
		return 0
	}
	//atMost(R) - atMost(L-1) = number of substrings between L and R
	return atMost(A, R) - atMost(A, L-1)
}

// atMost function returns the number of substrings with max value <= n
func atMost(A []int, n int) int {
	pre := 0
	res := 0
	for i := 0; i < len(A); i++ {
		if A[i] <= n {
			pre++
		} else {
			pre = 0
		}
		res += pre
	}
	return res
}
