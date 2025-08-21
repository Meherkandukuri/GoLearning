package main

import (
	"strings"
)

func areSentencesSimilar(sentence1, sentence2 string) bool {
	words1 := strings.Split(sentence1, " ")
	words2 := strings.Split(sentence2, " ")

	n1, n2 := len(words1), len(words2)
	i, j := 0, 0

	// Match from start
	for i < n1 && i < n2 && words1[i] == words2[i] {
		i++
	}
	// Match from end
	for j < n1-i && j < n2-i && words1[n1-1-j] == words2[n2-1-j] {
		j++
	}
	// If all words in the shorter sentence are matched from start and/or end
	return i+j == min1813(n1, n2)
}

func min1813(a, b int) int {
	if a < b {
		return a
	}
	return b
}
