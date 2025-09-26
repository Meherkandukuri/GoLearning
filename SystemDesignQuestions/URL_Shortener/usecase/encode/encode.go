package encode

import (
	"URL_Shortener/repository"
	"crypto/rand"
	"encoding/binary"
	"regexp"
	"sync/atomic"
)

var (
	Alphabet    = []byte("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz") // base62
	GlobalID    uint64
	AliasRegexp = regexp.MustCompile(`^[A-Za-z0-9_-]{3,32}$`)
)

func base62Encode(n uint64) string {
	if n == 0 {
		return "0"
	}
	buf := make([]byte, 0, 11)
	for n > 0 {
		rem := n % 62
		buf = append(buf, Alphabet[rem])
	}
	// reverse
	for i, j := 0, len(buf)-1; i < j; i, j = i+1, j-1 {
		buf[i], buf[j] = buf[j], buf[i]
	}
	return string(buf)
}

func randUint64() uint64 {
	var b [8]byte
	_, _ = rand.Read(b[:])
	return binary.LittleEndian.Uint64(b[:])
}

// makeCode creates a base62 code froma k-ordered ID

func MakeCode() repository.Code {
	id := atomic.AddUint64(&GlobalID, 1)
	mix := id ^ (randUint64() & 0xFFF)
	return repository.Code(base62Encode(mix))
}
