package Medium

import "slices"

func numFriendRequests(ages []int) int {

	if len(ages) == 0 {
		return 0
	}

	slices.SortFunc(ages, func(a, b int) int {
		return a - b
	})

	n := len(ages)
	fr := 0

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			if i == j {
				continue
			}
			if ages[j] <= int(0.5*float64(ages[i])+7.0) {
				continue
			}

			if ages[j] > ages[i] {
				continue
			}

			if ages[j] > 100 && ages[i] < 100 {
				continue
			}
			fr++
		}
	}

	return fr

}
