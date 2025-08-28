package domain

type GameState uint8

const (
	Waiting GameState = iota
	InProgress
	Finished
)
