package main

func flipAndInvertImage(image [][]int) [][]int {
	for i := 0; i < len(image); i++ {
		n := len(image[i])
		for j := 0; j < (n+1)/2; j++ {
			// Swap and invert in one step
			image[i][j], image[i][n-1-j] = image[i][n-1-j]^1, image[i][j]^1
		}
	}
	return image
}
