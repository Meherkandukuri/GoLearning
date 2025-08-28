package repository


type MemoryRepo struct {
	mu sync.Mutex
	store map[string]*domain.Game
}

func NewMemoryRepo() *MemoryRepo {
	return &MemoryRepo{store: make(map[string]*domain.Game)}
}

func (r *MemoryRepo) Save(g *domain.Game) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	// use history length as ID for simplicity
	id := "game1"
	r.store[id] = g
	return nil
}

func (r *MemoryRepo) Get(id string) (*domain.Game, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if g, ok := r.store[id]; ok {
		return g, nil
	}
	return nil, errors.New("not found")
}