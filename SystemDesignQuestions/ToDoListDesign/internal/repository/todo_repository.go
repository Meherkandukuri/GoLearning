package repository

import (
	"context"
	"github.com/Meherkandukuri/GoLearning/SystemDesignQuestions/ToDoListDesign/internal/domain"
)

type TodoRepository interface {
	Create(ctx context.Context, t *domain.Todo) error
	Find(ctx context.Context, id uint64) (*domain.Todo, error)
	List(ctx context.Context, offset, limit int) ([]domain.Todo, error)
	Update(ctx context.Context, t *domain.Todo) error
	Delete(ctx context.Context, id uint64) error
}
