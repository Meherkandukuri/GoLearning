package main

import "slices"

func bagOfTokensScore(tokens []int, power int) int {
	slices.Sort(tokens)
	left, right := 0, len(tokens)-1
	score, maxScore := 0, 0

	for left <= right {
		if tokens[left] <= power {
			power -= tokens[left]
			score++
			left++
			if score > maxScore {
				maxScore = score
			}
		} else if score > 0 {
			power += tokens[right]
			score--
			right--
		} else {
			break
		}
	}
	return maxScore
}
