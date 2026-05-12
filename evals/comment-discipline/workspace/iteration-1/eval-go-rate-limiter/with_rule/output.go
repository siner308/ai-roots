package ratelimiter

import (
	"sync"
	"time"
)

type Limiter struct {
	mu       sync.Mutex
	tokens   float64
	burst    float64
	rate     float64
	lastTick time.Time
}

func NewLimiter(ratePerSec int, burst int) *Limiter {
	return &Limiter{
		tokens:   float64(burst),
		burst:    float64(burst),
		rate:     float64(ratePerSec),
		lastTick: time.Now(),
	}
}

func (l *Limiter) Allow() bool {
	l.mu.Lock()
	defer l.mu.Unlock()

	now := time.Now()
	elapsed := now.Sub(l.lastTick).Seconds()
	l.lastTick = now

	l.tokens += elapsed * l.rate
	if l.tokens > l.burst {
		l.tokens = l.burst
	}

	if l.tokens < 1 {
		return false
	}

	l.tokens--
	return true
}
