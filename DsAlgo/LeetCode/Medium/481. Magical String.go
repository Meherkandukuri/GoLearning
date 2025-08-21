package Medium

func magicalString(n int) int {
	magical := make([]uint8, 1, n+2)
	magical[0] = 1
	var next uint8 = 2
	var count uint8 = 2
	index := 1
	for len(magical) <= n {
		magical = append(magical, next)
		if count == 2 {
			magical = append(magical, next)
		}
		next = 3 - next
		index++
		count = magical[index]
	}

	res := 0
	for i := 0; i < n; i++ {
		if magical[i] == 1 {
			res++
		}
	}
	return res
}
