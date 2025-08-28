package domain

type Move struct {
	Player PlayerID
	Col int
	Row int
}

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

func (m *Move) Undo(g *Game) {
	g.Board.UndoDrop(m.Col)
	g.State = InProgress
	g.Winner = Empty
	g.turnIdx = 1 - g.turnIdx
}