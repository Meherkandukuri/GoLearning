package main

import (
	"strings"
	"unicode"
)

func isPalindrome(s string) bool {

	s = formatToAphanumeric(s)

	l, r := 0, len(s)-1

	if len(s) < 2 {
		return true
	}

	for l < r {
		if s[l] != s[r] {
			return false
		}
		l++
		r--
	}
	return true
}

func formatToAphanumeric(s string) string {
	var builder strings.Builder
	for _, value := range s {
		if unicode.IsDigit(value) || unicode.IsLetter(value) {
			builder.WriteRune(unicode.ToLower(value))
		}
	}
	return builder.String()
}
