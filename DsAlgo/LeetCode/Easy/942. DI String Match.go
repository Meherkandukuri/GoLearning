package main

func diStringMatch(s string) []int {

	min := 0
	max := len(s)

	res := make([]int, len(s)+1)

	for i := 0; i < len(s); i++ {
		if s[i] == 'I' {
			res[i] = min
			min++
		} else {
			res[i] = max
			max--
		}
	}

	res[len(s)] = min // here you can use max as well instead of

	return res
}
