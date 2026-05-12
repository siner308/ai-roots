package baseline

import (
	"sync"
	"time"
)

// Limiter implements a token bucket rate limiter.
// Tokens are added at a fixed rate (ratePerSec tokens per second),
// up to a maximum of burst tokens. Each Allow() call consumes one token.
type Limiter struct {
	mu       sync.Mutex
	tokens   float64   // current number of available tokens
	maxBurst float64   // maximum token capacity
	rate     float64   // tokens added per nanosecond
	lastTick time.Time // timestamp of the last token refill
}

// NewLimiter creates a new token bucket Limiter.
// ratePerSec is the number of tokens added per second.
// burst is the maximum number of tokens the bucket can hold.
func NewLimiter(ratePerSec int, burst int) *Limiter {
	return &Limiter{
		tokens:   float64(burst), // start with a full bucket
		maxBurst: float64(burst),
		rate:     float64(ratePerSec) / float64(time.Second), // tokens per nanosecond
		lastTick: time.Now(),
	}
}

// Allow reports whether one token is available.
// If a token is available, it is consumed and Allow returns true.
// Otherwise Allow returns false immediately (non-blocking).
func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	// Refill tokens based on elapsed time since the last call.
	now := time.Now()
	elapsed := now.Sub(l.lastTick)
	l.lastTick = now

	l.tokens += float64(elapsed) * l.rate
	if l.tokens > l.maxBurst {
		l.tokens = l.maxBurst // cap at burst limit
	}

	// Consume one token if available.
	if l.tokens < 1 {
		return false
	}
	l.tokens--
	return true
}
