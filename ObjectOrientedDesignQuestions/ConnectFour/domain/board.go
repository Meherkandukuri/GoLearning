package domain

type Board struct {
	W, H    int
	cells   []PlayerID
	heights []int
}

func NewBoard(w, h int) *Board {
	return &Board{
		W:       w,
		H:       h,
		cells:   make([]PlayerID, w*h),
		heights: make([]int, w),
	}
}

func (b *Board) idx(r, c int) int {
	return r*b.W + c
}

func (b *Board) IsFull() bool {
	for c := 0; c < b.W; c++ {
		if b.heights[c] < b.H {
			return false
		}
	}
	return true
}


func (b *Board) At(r, c int) PlayerID {
	if r < 0 || r >= b.H || c < 0 || c >= b.W {
		return Empty
	}
	return b.cells[b.idx(r, c)]
}

func (b *Board) Drop(col int, p PlayerID) (row int, err error) {
	if col < 0 || col >= b.W {
		return -1, ErrInvalidColumn
	}
	if b.heights[col] >= b.H {
		return -1, ErrColumnFull
	}
	h := b.heights[col]
	b.cells[b.idx(h, col)] = p
	b.heights[col]++
	return h, nil
}

func (b *Board) UndoDrop(col int) int {
	b.heights[col]--
	row := b.heights[col]
	b.cells[b.idx(row, col)] = Empty
	return row
}
