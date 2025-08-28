package usecase


type GameUseCase struct {
	repo repository.GameRepository
}

func NewGameUseCase(r repository.GameRepository) *GameUseCase {
	return &GameUseCase{
		repo: r,
	}
}

func (u *GameUsecase) CreateGame(w, h, connectN int) (*domain.Game, error) {
	g := domain.NewGame(w, h, connectN)
	if err := u.repo.Save(g); err != nil {
		return nil, err
	}
	return g, nil
}

func (u *GameUsecase) PlayMove(gameID string, col int) (*domain.Move, error) {
	g, err := u.repo.Get(gameID)
	if err != nil {
		return nil, err
	}
	move, err := g.ApplyMove(col)
	if err != nil {
		return nil, err
	}
	if err := u.repo.Save(g); err != nil {
		return nil, err
	}
	return &move, nil
}
