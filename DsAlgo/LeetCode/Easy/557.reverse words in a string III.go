package main

import (
	"strings"
)

func reverseWords557(s string) string {

	wordsSlice := strings.Split(s, " ")

	for i, value := range wordsSlice {
		wordsSlice[i] = reverseString557(value)
	}

	return strings.Join(wordsSlice, " ")

}

func reverseString557(s string) string {

	runeSlice := []rune(s)

	for i, j := 0, len(runeSlice)-1; i < j; i, j = i+1, j-1 {
		runeSlice[i], runeSlice[j] = runeSlice[j], runeSlice[i]
	}

	return string(runeSlice)
}
