// Package domain contains the core logic for the Connect Four game.

package domain

// GameState represents the state of the game.
type GameState uint8

const (
	// Waiting indicates the game is waiting to start.
	Waiting GameState = iota
	// InProgress indicates the game is currently being played.
	InProgress
	// Finished indicates the game has ended.
	Finished
)
