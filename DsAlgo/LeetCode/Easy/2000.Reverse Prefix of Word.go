package main

import (
	"strings"
)

func reversePrefix(word string, ch rune) string {
	runes := []rune(word)
	chIndex := strings.IndexRune(word, ch)
	if chIndex == -1 {
		return word
	}
	// Reverse the prefix [0...chIndex]
	for i, j := 0, chIndex; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}













