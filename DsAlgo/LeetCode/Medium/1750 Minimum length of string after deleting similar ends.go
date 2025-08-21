package main

import (
	"strings"
)

func minimumLength(s string) int {

	for len(s) > 1 {
		found := -1
		if s[0] == s[len(s)-1] {
			found = 1
			s = strings.Trim(s, string(s[0]))
		}
		if found == -1 {
			return len(s)
		}
	}

	return len(s)

}
