package main

func shortestToChar(s string, c byte) []int {
	result := make([]int, len(s))

	for i := 0; i < len(s); i++ {
		shortest := len(s) // Initialize to max possible distance

		// Forward search
		for forward := i; forward < len(s); forward++ {
			if s[forward] == c {
				if forward-i < shortest {
					shortest = forward - i
				}
				break // No need to search further forward
			}
		}

		// Backward search
		for backward := i; backward >= 0; backward-- {
			if s[backward] == c {
				if i-backward < shortest {
					shortest = i - backward
				}
				break // No need to search further backward
			}
		}

		result[i] = shortest
	}

	return result
}
