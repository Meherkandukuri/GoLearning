package Medium

func sampleStats(count []int) []float64 {
	var (
		min, max, mode       int
		total, sum, maxCount int
		median               float64
	)

	n := len(count)
	foundMin := false

	// 1. Find min, max, mode, sum, total count
	for k := 0; k < n; k++ {
		c := count[k]
		if c > 0 {
			if !foundMin {
				min = k
				foundMin = true
			}
			max = k
			if c > maxCount {
				maxCount = c
				mode = k
			}
			sum += k * c
			total += c
		}
	}

	// 2. Find median
	// For median, walk through the counts, accumulating the running total
	// For odd total: find the (total/2+1)-th element
	// For even total: average the (total/2)-th and (total/2+1)-th elements

	mid1, mid2 := -1, -1
	if total%2 == 1 {
		mid1 = total/2 + 1
		mid2 = mid1
	} else {
		mid1 = total / 2
		mid2 = mid1 + 1
	}

	cnt := 0
	m1, m2 := -1, -1
	for k := 0; k < n; k++ {
		cnt += count[k]
		if m1 == -1 && cnt >= mid1 {
			m1 = k
		}
		if m2 == -1 && cnt >= mid2 {
			m2 = k
			break
		}
	}
	median = float64(m1+m2) / 2.0

	mean := float64(sum) / float64(total)

	return []float64{
		float64(min),
		float64(max),
		mean,
		median,
		float64(mode),
	}
}
