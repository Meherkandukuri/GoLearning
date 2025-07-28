package usecase

import (
	"context"
	"errors"
	"github.com/Meherkandukuri/GoLearning/SystemDesignQuestions/ToDoListDesign/internal/domain"
	"github.com/Meherkandukuri/GoLearning/SystemDesignQuestions/ToDoListDesign/internal/repository"
)

type TodoService struct {
	repo repository.TodoRepository
}

func NewTodoService(r repository.TodoRepository) *TodoService {
	return &TodoService{repo: r}
}

// Create adds a new Todo item after validating the title.
func (s *TodoService) Create(ctx context.Context, t *domain.Todo) error {
	if t.Title == "" {
		return errors.New("title required")
	}
	return s.repo.Create(ctx, t)
}

// Find retrieves a Todo item by its ID.
func (s *TodoService) Find(ctx context.Context, id uint64) (*domain.Todo, error) {
	return s.repo.Find(ctx, id)
}

// List returns a paginated list of Todo items.
func (s *TodoService) List(ctx context.Context, page, size int) ([]domain.Todo, error) {
	offset := (page - 1) * size
	return s.repo.List(ctx, offset, size)
}

// Update modifies an existing Todo item.
func (s *TodoService) Update(ctx context.Context, t *domain.Todo) error {
	if t.ID == 0 {
		return errors.New("invalid todo ID")
	}
	return s.repo.Update(ctx, t)
}

// Delete removes a Todo item by its ID.
func (s *TodoService) Delete(ctx context.Context, id uint64) error {
	if id == 0 {
		return errors.New("invalid todo ID")
	}
	return s.repo.Delete(ctx, id)
}
