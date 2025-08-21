package Medium

func rotateTheBox(boxGrid [][]byte) [][]byte {
	m, n := len(boxGrid), len(boxGrid[0])

	// Apply gravity to each row
	for i := 0; i < m; i++ {
		// Process from right to left
		empty := n - 1 // Track rightmost empty position

		for j := n - 1; j >= 0; j-- {
			if boxGrid[i][j] == '*' {
				// Reset empty position when we hit an obstacle
				empty = j - 1
			} else if boxGrid[i][j] == '#' {
				// If we found a stone and there's an empty space to the right
				if j < empty {
					// Move stone to empty position
					boxGrid[i][empty] = '#'
					boxGrid[i][j] = '.'
					empty--
				} else {
					// Stone can't move, update empty position
					empty = j - 1
				}
			}
			// If current cell is '.', we can just skip it
		}
	}

	// Rotate the grid 90 degrees clockwise
	rotated := make([][]byte, n)
	for i := 0; i < n; i++ {
		rotated[i] = make([]byte, m)
		for j := 0; j < m; j++ {
			rotated[i][j] = boxGrid[m-1-j][i]
		}
	}

	return rotated
}
