package main

import (
	"log"
	"net/http"
	"os"

	repo "URL_Shortener/repository"
	handler "URL_Shortener/api"

)

func main() {
	baseURL := os.Getenv("BASE_URL")
	store := repo.NewMemStore()
	s := handler.NewServer(store, baseURL)

	http.HandleFunc("/api/v1/shorten", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
			return
		}
		s.Shorten(w, r)
	})

	http.HandleFunc("/api/v1/stats/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		}
		s.Stats(w, r)
	})

	// catch-all for redirecting short URLs
	http.HandleFunc("/", s.Redirect)

	addr := ":8080"
	log.Printf("URL Shortener listening on %s (BASE_URL=%s)", addr, baseURL)
	log.Fatal(http.ListenAndServe(addr, nil))
}
