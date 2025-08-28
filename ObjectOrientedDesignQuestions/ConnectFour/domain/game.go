// Package domain contains the core logic for the Connect Four game.

package domain

import "sync"

// Game represents the state of a Connect Four game.
// mu ensures thread-safe operations.
// Board is the game board.
// Rules defines the win-checking logic.
// Players are the two players in the game.
// turnIdx tracks whose turn it is.
// State is the current state of the game.
// Winner is the winner of the game.
// History is the list of moves made.
type Game struct {
	mu      sync.Mutex
	Board   *Board
	Rules   WinChecker
	Players [2]PlayerID
	turnIdx int
	State   GameState
	Winner  PlayerID
	History []Move
}

// NewGame creates a new game with the specified dimensions and win condition.
func NewGame(w, h, connectN int) *Game {
	return &Game{
		Board:   NewBoard(w, h),
		Rules:   ConnectN{N: connectN},
		Players: [2]PlayerID{Player1, Player2},
		State:   InProgress,
	}
}

// Current returns the current player.
func (g *Game) Current() PlayerID {
	return g.Players[g.turnIdx]
}

// ApplyMove applies a move to the game state.
func (g *Game) ApplyMove(col int) (Move, error) {
	g.mu.Lock()
	defer g.mu.Unlock()
	m := Move{Player: g.Current(), Col: col}
	if err := m.Do(g); err != nil {
		return Move{}, err
	}
	g.History = append(g.History, m)
	return m, nil
}

// Undo undoes the last move.
func (g *Game) Undo() bool {
	g.mu.Lock()
	defer g.mu.Unlock()
	if len(g.History) == 0 {
		return false
	}
	last := g.History[len(g.History)-1]
	last.Undo(g)
	g.History = g.History[:len(g.History)-1]
	return true
}
