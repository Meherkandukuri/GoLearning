package domain

import "time"

type ShortenRequest struct {
	URL        string `json:"url"`
	Custom     string `json:"custom_alias,omitempty"`
	ExpireSecs int64  `json:"expire_in_seconds,omitempty"`
}

type ShortenResponse struct {
	Code      string     `json:"code"`
	ShortURL  string     `json:"short_url"`
	LongURL   string     `json:"long_url"`
	CreatedAt time.Time  `json:"created_at"`
	ExpiresAt *time.Time `json:"expires_at,omitempty"`
}
