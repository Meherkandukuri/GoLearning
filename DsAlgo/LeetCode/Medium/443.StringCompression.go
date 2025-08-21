package Medium

import "strconv"

func compress(chars []byte) int {

	n := len(chars)
	i := 0
	idx := 0

	for i < n {
		ch := chars[i]
		count := 0
		for i < n && chars[i] == ch {
			count++
			i++
		}
		if count == 1 {
			chars[idx] = ch
			idx++
		} else {
			chars[idx] = ch
			idx++
			for _, digit := range []byte(strconv.Itoa(count)) {
				chars[idx] = digit
				idx++
			}
		}
	}

	return idx
}
