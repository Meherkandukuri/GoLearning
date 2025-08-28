package domain

import "errors"

var (
	ErrInvalidColumn = errors.New("invalid column")
	ErrColumnFull    = errors.New("column is full")
	ErrWrongTurn     = errors.New("not this player's turn")
	ErrGameFinished  = errors.New("game already finished")
)
