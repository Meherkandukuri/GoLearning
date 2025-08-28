package domain

import "sync"

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

func NewGame(w, h, connectN int) *Game {
	return &Game{
		Board: NewBoard(w, h),
		Rules: ConnectN{N: connectN},
		Players: [2]PlayerID{Player1, Player2},
		State: InProgress,
	}
}

func (g *Game) Current() PlayerID {
	return g.Players[g.turnIdx]
}

func (g *Game) ApplyMove(col int) (Move, error) {
	g.mu.Lock()
	defer g.mu.Unlock()  
	m := Move{Player:g.Current(), Col: col}
	if err := m.Do(g); err != nil {
		return Move{}, err
	}
	g.History = append(g.History, m)
	return m, nil
}

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