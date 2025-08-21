package main

var skipCharCount int

func validPalindrome(s string) bool {
	return isPalindromewithSkip(s, 0, len(s)-1, 0, 1)
}

func isPalindromewithSkip(s string, left, right, skipCount, maxSkipCount int) bool {
	for left < right {
		if s[left] != s[right] {
			// if already skipped one character, return false
			if skipCount == maxSkipCount {
				return false
			}
			return isPalindromewithSkip(s, left+1, right, 1, 1) || isPalindromewithSkip(s, left, right-1, 1, 1)
		}
		left++
		right--
	}

	return true
}
