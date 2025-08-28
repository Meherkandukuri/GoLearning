package repsitory

import "connect4/domain"

type GameRepository interface {
	Save(game *domain.Game) error
	Get(id string) (*domain.Game, error)
}

