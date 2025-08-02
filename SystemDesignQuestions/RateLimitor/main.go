package main

func main() {
	//-------------------LeakyBucketMain:--------------//
	/*
		leakyBucketInst := NewLeakyBucket(5, 500*time.Millisecond)
		for range 10 {
			if leakyBucketInst.Allow() {
				fmt.Println("Request allowed")
			} else {
				fmt.Println("Request not allowed")
			}
			time.Sleep(200 * time.Millisecond)
		}
	*/
	//----------------------------------------------------//
	//-------------------SlidingWindowLogMain:--------------//
	/*
		limiter := NewSlidingWindowLimiter(5, 3*time.Second)
		for i := 1; i <= 10; i++ {
			if limiter.Allow() {
				fmt.Printf("Request %d: Allowed\n", i)
			} else {
				fmt.Printf("Request %d: Denied\n", i)
			}
			time.Sleep(500 * time.Millisecond)
		}
	*/
	//----------------------------------------------------//
	//-------------------FixedWindowMain:--------------//
	/*
		rateLimiter := NewRatelimiter_WA(5, 2*time.Second)
			for range 10 {
				if rateLimiter.Allow_WA() {
					fmt.Println("Request allowed.")
				} else {
					fmt.Println("Request not allowed.")
				}
				time.Sleep(200 * time.Millisecond)
			}
	*/
	//-------------------TokenBucketMain:--------------//
	/*
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
	*/
}
