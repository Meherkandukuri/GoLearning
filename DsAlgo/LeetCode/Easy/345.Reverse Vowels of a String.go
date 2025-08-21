package main

func reverseVowels(s string) string {
	left, right := 0, len(s)-1

	runeSlice := convertToSlice(s)

	for left < right {

		for left < right && !isVowel(rune(runeSlice[left])) {
			left++
		}

		for left < right && !isVowel(rune(runeSlice[right])) {
			right--
		}

		if left < right {
			runeSlice[right], runeSlice[left] = runeSlice[left], runeSlice[right]
			left++
			right--
		}
	}

	return convertToString(runeSlice)

}

func isVowel(b rune) bool {
	switch b {
	case 'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U': // Directly compare runes
		return true
	}
	return false
}

func convertToSlice(a string) []rune {

	var result = make([]rune, len(a))

	for i, value := range a {
		result[i] = value
	}
	return result

}

func convertToString(r []rune) string {
	var s string
	for _, value := range r {
		s += string(value)
	}
	return s
}
