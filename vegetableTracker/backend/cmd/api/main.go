package main

import (
	"context"
	"flag"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/auth"
	"github.com/Meherkandukuri/vegetableTracker/backend/internal/handlers"
	"github.com/Meherkandukuri/vegetableTracker/backend/internal/middleware"
	"github.com/Meherkandukuri/vegetableTracker/backend/internal/store"
)

func main() {
	var (
		addr      = flag.String("addr", ":8080", "HTTP listen address")
		dsn       = flag.String("dsn", os.Getenv("VT_DATABASE_DSN"), "Postgres DSN")
		jwtSecret = flag.String("jwt-secret", os.Getenv("VT_JWT_SECRET"), "JWT secret")
	)
	flag.Parse()

	if *dsn == "" {
		log.Fatal("missing DSN (VT_DATABASE_DSN)")
	}
	if *jwtSecret == "" {
		log.Fatal("missing JWT secret (VT_JWT_SECRET)")
	}

	db, err := store.Open(*dsn)
	if err != nil {
		log.Fatalf("open db: %v", err)
	}
	defer db.Conn.Close()

	authSvc := auth.NewService(*jwtSecret)
	h := handlers.New(db, authSvc)

	r := chi.NewRouter()
	r.Use(cors.Handler(cors.Options{AllowedOrigins: []string{"*"}, AllowedMethods: []string{"GET", "POST", "PUT", "DELETE"}, AllowedHeaders: []string{"Authorization", "Content-Type"}}))
	r.Use(middleware.RequestLogger())

	r.Mount("/api", h.RoutesWithAuth(middleware.AuthMiddleware(authSvc)))

	srv := &http.Server{Addr: *addr, Handler: r, ReadHeaderTimeout: 10 * time.Second}
	log.Printf("listening on %s", *addr)
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("server: %v", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	_ = srv.Shutdown(ctx)
}
