package main

import (
	"strings"
	"unicode"
)

func reverseOnlyLetters(s string) string {
	left, right := 0, len(s)-1
	letterSlice := make([]rune, len(s))

	for index, value := range s {
		letterSlice[index] = value
	}

	for left < right {
		for !unicode.IsLetter(letterSlice[left]) {
			left++
		}
		for !unicode.IsLetter(letterSlice[right]) {
			right--
		}

		if left < right {
			letterSlice[left], letterSlice[right] = letterSlice[right], letterSlice[left]
		}
		left++
		right--
	}

	return sliceToString(letterSlice)

}

func sliceToString(r []rune) string {
	var builder strings.Builder

	for _, value := range r {
		builder.WriteRune(value)
	}

	return builder.String()
}
