package main

func duplicateZeros(arr []int) {

	zeros := 0
	n := len(arr)

	for _, val := range arr {
		if val == 0 {
			zeros++
		}
	}

	for i := n - 1; i >= 0; i-- {
		if arr[i] == 0 {
			if zeros+i < len(arr) {
				arr[zeros+i] = 0
			}

			if zeros+i-1 < len(arr) {
				arr[zeros+i-1] = 0
			}

			zeros--
		} else if zeros+i < len(arr) {
			arr[zeros+i] = arr[i]
		}
	}

}
