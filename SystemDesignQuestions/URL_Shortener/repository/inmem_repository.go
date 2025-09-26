package repository

import (
	"fmt"
	"sync"
	"time"
)

type Code string

type ShortURL struct {
	Code       Code     `json:"code" bson:"code"`
	LongURL    string     `json:"long_url" bson:"long_url"`
	CreatedAt  time.Time  `json:"created_at" bson:"created_at"`
	ExpiresAt  *time.Time `json:"expires_at,omitempty" bson:"expires_at,omitempty"`
	IsActive   bool       `json:"is_active" bson:"is_active"`
	ClickCount uint64     `json:"click_count" bson:"click_count"`
	LastAccess *time.Time `json:"last_access,omitempty" bson:"last_access,omitempty"`
}

type Store interface {
	Create(s ShortURL) error
	Get(code string) (*ShortURL, error)
	IncrementClicks(code string) (ShortURL, bool)
	Deactivate(code string) bool
}

type MemStore struct {
	mu   sync.RWMutex
	data map[Code]ShortURL
}

func NewMemStore() *MemStore {
	return &MemStore{
		data: make(map[Code]ShortURL),
	}
}

func (m *MemStore) Create(s ShortURL) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	if _, exists := m.data[s.Code]; exists {
		return fmt.Errorf("code already exists: %s", s.Code)
	}
	return nil
}

func (m *MemStore) Get(code Code) (ShortURL, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()
	s, ok := m.data[code]
	return s, ok
}

func (m *MemStore) IncrementClicks(code Code) (ShortURL, bool) {
	m.mu.Lock()
	defer m.mu.Unlock()
	s, ok := m.data[code]
	if !ok {
		return ShortURL{}, false
	}
	s.ClickCount++
	now := time.Now()
	s.LastAccess = &now
	m.data[code] = s
	return s, true
}

func (m *MemStore) Deactivate(code Code) bool {
	m.mu.Lock()
	defer m.mu.Unlock()
	s, ok := m.data[code]
	if !ok {
		return false
	}
	s.IsActive = false
	m.data[code] = s
	return true
}


































