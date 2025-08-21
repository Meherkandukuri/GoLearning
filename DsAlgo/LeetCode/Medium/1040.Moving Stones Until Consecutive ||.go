package Medium

import "slices"

func numMovesStonesII(stones []int) []int {

	slices.SortFunc(stones, func(a, b int) int {
		return a - b
	})

	n := len(stones)
	low := n
	high := max(stones[n-1]-stones[1]+1-(n-1), stones[n-2]+1-stones[0]-(n-1))

	i := 0

	for j := range n {
		for stones[j]-stones[i] >= n {
			i++
		}
		if j-i+1 == n-1 && stones[j]-stones[i] == n-2 {
			if low > 2 {
				low = 2
			}
		} else {
			if low > n-(j-i+1) {
				low = n - (j - i + 1)
			}
		}
	}
	return []int{low, high}

}

func maxab(a, b int) int {
	if a > b {
		return a
	}
	return b
}
