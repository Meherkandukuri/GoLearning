package domain

import "errors"

// Package domain contains the core logic for the Connect Four game.
//
// ErrInvalidColumn is returned when a move is made in an invalid column.
// ErrColumnFull is returned when a move is made in a full column.
// ErrWrongTurn is returned when a player tries to play out of turn.
// ErrGameFinished is returned when a move is made after the game is finished.

var (
	ErrInvalidColumn = errors.New("invalid column")
	ErrColumnFull    = errors.New("column is full")
	ErrWrongTurn     = errors.New("not this player's turn")
	ErrGameFinished  = errors.New("game already finished")
)
