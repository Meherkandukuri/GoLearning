package domain

type WinChecker interface {
	WinLength() int
	Won(b *Board, lastRow, lastCol int, p PlayerID) bool
}

type ConnectN struct{ N int }

func (c ConnectN) WinLength() int { return c.N }

func (c ConnectN) Won(b *Board, r, col int, p PlayerID) bool {
	dirs := [][2]int{{1, 0}, {0, 1}, {1, 1}, {1, -1}}
	for _, d := range dirs {
		count := 1
		count += countDir(b, r, col, d[0], d[1], p)
		count += countDir(b, r, col, -d[0], -d[1], p)
		if count >= c.N {
			return true
		}
	}
	return false
}

func countDir(b *Board, r, c, dr, dc int, p PlayerID) int {
	cnt := 0
	for rr, cc := r+dr, c+dc; rr >= 0 && rr < b.H && cc >= 0 && cc < b.W && b.At(rr, cc) == p; {
		cnt++
		rr += dr
		cc += dc
	}
	return cnt
}
