package domain
// Package domain contains the core logic for the Connect Four game.
// It defines the game board, player actions, and the rules for winning.


// Board represents the game board with its dimensions, cell states, and column heights.
// W and H are the width and height of the board.
// cells is a 1D slice storing the state of each cell.
// heights tracks the current height of each column.
type Board struct {
	W, H    int
	cells   []PlayerID
	heights []int
}

// NewBoard creates a new Board with the specified width and height.
// It initializes the cells and heights slices to their starting values.
func NewBoard(w, h int) *Board {
	return &Board{
		W:       w,
		H:       h,
		cells:   make([]PlayerID, w*h),
		heights: make([]int, w),
	}
}

// idx converts 2D coordinates (row, column) to a 1D index for the cells slice.
// This is used to access or modify the state of a specific cell on the board.
func (b *Board) idx(r, c int) int {
	return r*b.W + c
}

// IsFull checks if the board is completely filled.
// It does this by checking if each column has reached the maximum height.
func (b *Board) IsFull() bool {
	for c := 0; c < b.W; c++ {
		if b.heights[c] < b.H {
			return false
		}
	}
	return true
}

// At returns the player occupying a specific cell, or Empty if out of bounds.
// This is used to query the state of the board at a given position.
func (b *Board) At(r, c int) PlayerID {
	if r < 0 || r >= b.H || c < 0 || c >= b.W {
		return Empty
	}
	return b.cells[b.idx(r, c)]
}

// Drop places a player's token in the specified column.
// It returns the row where the token landed, or an error if the move is invalid.
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

// UndoDrop removes the top token from the specified column, effectively undoing the last Drop action.
// It returns the row from which the token was removed.
func (b *Board) UndoDrop(col int) int {
	b.heights[col]--
	row := b.heights[col]
	b.cells[b.idx(row, col)] = Empty
	return row
}
