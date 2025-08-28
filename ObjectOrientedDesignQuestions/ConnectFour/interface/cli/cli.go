package cli

import (
	"bufio"
	"connect4/usecase"
	"fmt"
	"os"

	"github.com/MeherKandukuri/GoLearning/ObjectOrientedDesignQuestions/ConnectFour/domain"
)

func RunCLI(uc *usecase.GameUsecase) {
	game, _ := uc.CreateGame(7, 6, 4)

	scanner := bufio.NewScanner(os.Stdin)
	for game.State == 1 { // InProgress
		fmt.Printf("Player %d, enter column: ", game.Current())
		scanner.Scan()
		var col int
		fmt.Sscan(scanner.Text(), &col)
		_, err := game.ApplyMove(col)
		if err != nil {
			fmt.Println("Error:", err)
		}
		printBoard(game.Board)
		if game.State == 2 {
			fmt.Println("Winner:", game.Winner)
		}
	}
}

func printBoard(b *domain.Board) {
	for r := b.H - 1; r >= 0; r-- {
		for c := 0; c < b.W; c++ {
			fmt.Print("|", b.At(r, c))
		}
		fmt.Println("|")
	}
	fmt.Println()
}
