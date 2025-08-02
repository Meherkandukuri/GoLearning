package main

import (
	"sync"
	"time"
)

/// ********** Rate Limiting using Sliding Window Log ********** ///
// Keep a log (e.g., a slice of timestamps) and remove entries older than window.

type SlidingWindowLimiter struct {
	mu       sync.Mutex
	limit    int
	window   time.Duration
	requests []time.Time
}

func NewSlidingWindowLimiter(limit int, window time.Duration) *SlidingWindowLimiter {
	return &SlidingWindowLimiter{
		limit:  limit,
		window: window,
	}
}

func (rl *SlidingWindowLimiter) Allow() bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()

	now := time.Now()
	cutoff := now.Add(-rl.window)

	// Remove old requests outside the time window
	i := 0
	for _, t := range rl.requests {
		if t.After(cutoff) {
			break
		}
		i++
	}
	rl.requests = rl.requests[i:]

	// Allow if under limit
	if len(rl.requests) < rl.limit {
		rl.requests = append(rl.requests, now)
		return true
	}

	return false
}
