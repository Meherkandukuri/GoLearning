package main

import (
	"fmt"
	"sync"
	"time"
)

/// ********** Rate Limiting using Fixed Window Algorithm ********** ///
// Following is a simple implementation of a rate limiter using the fixed window algorithm.
// This implementation allows a fixed number of requests within a specified time window.
// If the limit is reached, subsequent requests are denied until the next window starts.
// Issues: Burst at boundaries: Users can send limit requests at the end of one window and another limit immediately at the start of the next.
// For Time: 1.9s → 5 requests
//Time: 2.1s → window resets → 5 more
//Total: 10 requests in 200ms.

type RateLimiter_WA struct {
	mu        sync.Mutex
	count     int
	limit     int
	window    time.Duration
	resetTime time.Time
}

func NewRatelimiter_WA(limit int, window time.Duration) *RateLimiter_WA {
	return &RateLimiter_WA{
		limit:  limit,
		window: window,
	}
}

func (rl *RateLimiter_WA) Allow_WA() bool {
	rl.mu.Lock()
	defer rl.mu.Unlock()
	now := time.Now()
	if now.After(rl.resetTime) {
		rl.resetTime = now.Add(rl.window)
		rl.count = 0
	}
	if rl.count < rl.limit {
		rl.count++
		return true
	}
	return false
}

func main() {
	rateLimiter := NewRatelimiter_WA(5, 2*time.Second)
	for range 10 {
		if rateLimiter.Allow_WA() {
			fmt.Println("Request allowed.")
		} else {
			fmt.Println("Request not allowed.")
		}
		time.Sleep(200 * time.Millisecond)
	}
}
