package main

import (
	"fmt"
	"math"
	"os"
	"sync"
	"text/tabwriter"
	"time"
)

// producer simulates a writer that locks and unlocks the mutex multiple times.
// It represents a goroutine that performs write operations.
func producer(wg *sync.WaitGroup, l sync.Locker) {
	defer wg.Done()
	for i := 5; i > 0; i-- {
		l.Lock()
		l.Unlock()
		time.Sleep(time.Second)
	}
}

// observer simulates a reader that acquires the lock once.
// It represents a goroutine that performs read operations.
func observer(wg *sync.WaitGroup, l sync.Locker) {
	defer wg.Done()
	l.Lock()
	defer l.Unlock()
}

// test runs one producer and multiple observers, measuring the time taken.
// It compares the performance of sync.Mutex and sync.RWMutex under concurrent access.
func test(count int, mutex, rwMutex sync.Locker) time.Duration {
	var wg sync.WaitGroup
	wg.Add(count + 1)
	beginTestTime := time.Now()
	go producer(&wg, mutex)
	for i := count; i > 0; i-- {
		go observer(&wg, rwMutex)
	}
	wg.Wait()
	return time.Since(beginTestTime)
}

func main() {
	// Create a RWMutex to be used for both read and write locking.
	var m sync.RWMutex
	// Setup a tabwriter for formatted output.
	tw := tabwriter.NewWriter(os.Stdout, 0, 1, 2, ' ', 0)
	defer tw.Flush()
	fmt.Println("Programme to compare sync.RWMutex and sync.Mutex has started ....")
	fmt.Fprintf(tw, "Readers\tRWMutex\tMutex\n")
	// Run tests with increasing numbers of readers.
	for i := 1; i < 10; i++ {
		count := int(math.Pow(2, float64(i)))
		// Test RWMutex with multiple readers.
		rwTime := test(count, &m, m.RLocker())
		// Test Mutex with multiple readers.
		mtxTime := test(count, &m, &m)
		// Output the results.
		fmt.Fprintf(tw, "%d\t%v\t%v\n", count, rwTime, mtxTime)
	}
}
