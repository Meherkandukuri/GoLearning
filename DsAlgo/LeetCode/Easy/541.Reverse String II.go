package main

import (
	"slices"
	"strings"
)

func reverseStr(s string, k int) string {
	strSlice := strings.Split(s, "")
	n := len(s)

	if n >= 2*k {
		sliceLen := 2 * k
		reverseLen := k

		for i := 0; i < n; i += sliceLen {
			end := i + reverseLen
			if end > n {
				end = n
			}
			slices.Reverse(strSlice[i:end])
		}
		return strings.Join(strSlice, "")
	} else if k <= n && n < 2*k {
		slices.Reverse(strSlice[:k])
		return strings.Join(strSlice, "")
	} else {
		slices.Reverse(strSlice)
		return strings.Join(strSlice, "")
	}

}
