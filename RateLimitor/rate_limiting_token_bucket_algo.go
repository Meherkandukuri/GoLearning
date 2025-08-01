package main

import (
	"fmt"
	"time"
)

type RateLimiter struct {
	tokens      chan struct{}
	refillRate  int
	refillTimer *time.Ticker
	quit        chan struct{}
}

func NewRateLimiter(capacity, refillRate int, refillInterval time.Duration) *RateLimiter {
	rl := &RateLimiter{
		tokens:      make(chan struct{}, capacity),
		refillRate:  refillRate,
		refillTimer: time.NewTicker(refillInterval),
		quit:        make(chan struct{}),
	}

	for i := 0; i < capacity; i++ {
		rl.tokens <- struct{}{}
	}

	go rl.startRefill()
	return rl
}

func (rl *RateLimiter) startRefill() {
	for {
		select {
		case <-rl.refillTimer.C:
			for i := 0; i < rl.refillRate; i++ {
				select {
				case rl.tokens <- struct{}{}:
				default:
					// channel is full
				}
			}
		case <-rl.quit:
			return
		}
	}
}

func (rl *RateLimiter) Allow() bool {
	select {
	case <-rl.tokens:
		return true
	default:
		return false
	}
}

func (rl *RateLimiter) Stop() {
	close(rl.quit)
	rl.refillTimer.Stop()
}

func main() {
	rl := NewRateLimiter(5, 5, time.Second)
	defer rl.Stop()

	for i := 0; i < 15; i++ {
		if rl.Allow() {
			fmt.Println("Request allowed")
		} else {
			fmt.Println("Request denied")
		}
		time.Sleep(200 * time.Millisecond)
	}
}
