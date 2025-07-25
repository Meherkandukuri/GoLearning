// internal/domain/todo.go
package domain

import "time"

type TodoStatus string

const (
	StatusOpen   TodoStatus = "OPEN"
	StatusClosed TodoStatus = "CLOSED"
)

type Todo struct {
	ID          uint64     `json:"id" gorm:"primaryKey"`
	Title       string     `json:"title" gorm:"size:120;not null"`
	Description string     `json:"description,omitempty" gorm:"size:500"`
	Status      TodoStatus `json:"status" gorm:"type:varchar(10);default:'OPEN'"`
	DueDate     *time.Time `json:"dueDate,omitempty"`
	CreatedAt   time.Time  `json:"createdAt"`
	UpdatedAt   time.Time  `json:"updatedAt"`
}
