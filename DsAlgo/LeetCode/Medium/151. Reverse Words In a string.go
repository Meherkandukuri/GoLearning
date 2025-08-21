package main

import "strings"

func reverseWords(s string) string {

	wordSlice := strings.Split(s, " ")
	resultSlice := []string{}

	for i := len(wordSlice) - 1; i >= 0; i-- {
		if wordSlice[i] != " " && wordSlice[i] != "" {
			resultSlice = append(resultSlice, wordSlice[i])
		}
	}
	return strings.Join(resultSlice, " ")
}
