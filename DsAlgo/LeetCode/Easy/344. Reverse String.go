package main

func reverseString(s []byte) {

	left, right := 0, len(s)
	for left < right {
		s[left], s[right] = s[right], s[left]
		left++
		right--
	}

}
