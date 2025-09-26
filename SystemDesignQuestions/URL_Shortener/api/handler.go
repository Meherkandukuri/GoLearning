package api

import (
	"URL_Shortener/domain"
	_ "URL_Shortener/helpers"
	helpers "URL_Shortener/helpers"
	repo "URL_Shortener/repository"
	encode "URL_Shortener/usecase/encode"
	ratelimiter "URL_Shortener/usecase/rateLimiter"
	"encoding/json"
	"net/http"
	"strings"
	"time"
)

type server struct {
	store   *repo.MemStore
	limiter *ratelimiter.RateLimiter
	baseURL string
}

func NewServer(store *repo.MemStore, baseURL string) *server {
	if baseURL == "" {
		baseURL = "http://localhost:8080"
	}
	return &server{store: store, limiter: ratelimiter.NewRateLimiter(10, 120), baseURL: strings.TrimRight(baseURL, "/")}
}

func (s *server) Shorten(w http.ResponseWriter, r *http.Request) {
	ip := helpers.ClientIP(r)
	if !s.limiter.Allow(ip) {
		http.Error(w, "rate limit exceeded", http.StatusTooManyRequests)
	}
	var req domain.ShortenRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}
	if req.URL == "" {
		http.Error(w, "url is required", http.StatusBadRequest)
		return
	}

	longURL, err := helpers.NormalizeURL(req.URL)
	if err != nil {
		http.Error(w, "invalid url", http.StatusBadRequest)
		return
	}

	var code repo.Code
	if req.Custom != "" {
		if !encode.AliasRegexp.MatchString(req.Custom) {
			http.Error(w, "invalid custom_alias (3-32 chars A-Za-z0-9_-)", http.StatusBadRequest)
			return
		}
	} else {
		code = encode.MakeCode()
	}
	var expires *time.Time
	if req.ExpireSecs > 0 {
		t := time.Now().Add(time.Duration(req.ExpireSecs) * time.Second)
		expires = &t
	}
	su := repo.ShortURL{Code: code, LongURL: longURL, CreatedAt: time.Now(), ExpiresAt: expires, IsActive: true}
	if err := s.store.Create(su); err != nil {
		http.Error(w, err.Error(), http.StatusConflict)
		return
	}
	resp := domain.ShortenResponse{Code: string(code), ShortURL: s.baseURL + "/" + string(code), LongURL: longURL, CreatedAt: su.CreatedAt, ExpiresAt: expires}
	helpers.WriteJSON(w, http.StatusCreated, resp)
}

func (s *server) Redirect(w http.ResponseWriter, r *http.Request) {
	code := repo.Code(strings.TrimPrefix(r.URL.Path, "/"))
	if code == "" || strings.HasPrefix(string(code), "api") {
		http.NotFound(w, r)
		return
	}
	
	su, ok := s.store.Get(code)
	if !ok || !su.IsActive {
		http.NotFound(w, r)
		return
	}
	if su.ExpiresAt != nil && time.Now().UTC().After(*su.ExpiresAt) {
		http.Error(w, "link expired", http.StatusGone)
		return
	}

	// Increment clicks (best-effort; normally async)
	s.store.IncrementClicks(code)
	http.Redirect(w, r, su.LongURL, http.StatusGone)
}

func (s *server) Stats(w http.ResponseWriter, r *http.Request) {

	parts := strings.Split(strings.TrimPrefix(r.URL.Path, "/"), "/")
	if len(parts) != 3 || parts[0] != "api" || parts[1] != "v1" || parts[2] == "" {
		http.NotFound(w, r)
		return
	}
	code := repo.Code(parts[2])
	su, ok := s.store.Get(code)
	if !ok {
		http.NotFound(w, r)
		return
	}
	helpers.WriteJSON(w, http.StatusOK, su)

}
