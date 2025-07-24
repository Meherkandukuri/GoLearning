package main

import (
	"fmt"
	"math"
	"os"
	"sync"
	"text/tabwriter"
	"time"
)

func producer(wg *sync.WaitGroup, l sync.Locker) {
	defer wg.Done()
	for i := 5; i > 0; i-- {
		l.Lock()
		l.Unlock()
		time.Sleep(time.Second)
	}
}

func observer(wg *sync.WaitGroup, l sync.Locker) {
	defer wg.Done()
	l.Lock()
	defer l.Unlock()
}

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
	var m sync.RWMutex
	tw := tabwriter.NewWriter(os.Stdout, 0, 1, 2, ' ', 0)
	defer tw.Flush()
	fmt.Println("Programme to compare sync.RWMutex and sync.Mutex has started ....")
	fmt.Fprintf(tw, "Readers\tRWMutex\tMutex\n")
	for i := 1; i < 10; i++ {
		count := int(math.Pow(2, float64(i)))
		rwTime := test(count, &m, m.RLocker())
		mtxTime := test(count, &m, &m)
		fmt.Fprintf(tw, "%d\t%v\t%v\n", count, rwTime, mtxTime)
	}
}
