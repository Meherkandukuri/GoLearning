package main

import (
	"connect4/interface/cli"
	"connect4/repository"
	"connect4/usecase"
)

func main() {
	repo := repository.NewMemoryRepo()
	uc := usecase.NewGameUsecase(repo)
	cli.RunCLI(uc)
}
