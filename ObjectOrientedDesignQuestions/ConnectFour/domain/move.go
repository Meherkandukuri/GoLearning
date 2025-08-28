package domain

// Move represents a player's move in the game.
// Player is the player making the move.
// Col is the column where the move is made.
// Row is the row where the move lands.
type Move struct {
	Player PlayerID
	Col    int
	Row    int
}

// Do executes the move, updates the game state, and checks for a winner.
// It returns an error if the move is invalid.
func (m *Move) Do(g *Game) error {
	if g.State == Finished {
		return ErrGameFinished
	}
	if g.Current() != m.Player {
		return ErrWrongTurn
	}
	row, err := g.Board.Drop(m.Col, m.Player)
	if err != nil {
		return err
	}
	m.Row = row

	if g.Rules.Won(g.Board, row, m.Col, m.Player) {
		g.State = Finished
		g.Winner = m.Player
	} else if g.Board.IsFull() {
		g.State = Finished
		g.Winner = Empty
	} else {
		g.turnIdx = 1 - g.turnIdx
	}
	return nil
}

// Undo reverts the move and updates the game state.
// It resets the row, changes the game state to in progress,
// clears the winner, and switches the turn to the other player.
func (m *Move) Undo(g *Game) {
	g.Board.UndoDrop(m.Col)
	g.State = InProgress
	g.Winner = Empty
	g.turnIdx = 1 - g.turnIdx
}
