package RateLimiter

import (
	"sync"
	"time"
)

type bucket struct {
	tokens     int
	lastRefill time.Time
}

type RateLimiter struct {
	mu       sync.Mutex
	buckets  map[string]*bucket
	capacity int
	ratePerS float64
}

func NewRateLimiter(capacity int, ratePerMinute int) *RateLimiter {
	return &RateLimiter{buckets: make(map[string]*bucket), capacity: capacity, ratePerS: float64(ratePerMinute) / 60.0}
}

func (rl *RateLimiter) Allow(key string) bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()
	now := time.Now()

	b, ok := rl.buckets[key]
	if !ok {
		b = &bucket{tokens: rl.capacity, lastRefill: time.Now()}
		rl.buckets[key] = b
		return true
	}
	// refill
	delta := now.Sub(b.lastRefill).Seconds() * rl.ratePerS
	if delta >= 1 {
		b.tokens = min(rl.capacity, b.tokens+int(delta))
		b.lastRefill = now
	}
	if b.tokens <= 0 {
		return false
	}
	b.tokens--
	return true
}

func min(a, b int) int {
	if a < b {
		return a
	}
	return b
}
