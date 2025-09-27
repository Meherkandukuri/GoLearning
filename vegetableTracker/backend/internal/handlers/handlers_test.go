package handlers

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/auth"
	mw "github.com/Meherkandukuri/vegetableTracker/backend/internal/middleware"
)

func TestAuthMiddleware_injectsUserID(t *testing.T) {
	authSvc := auth.NewService("test-secret")
	token, err := authSvc.NewToken(7)
	if err != nil {
		t.Fatalf("new token: %v", err)
	}

	handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		uid := mw.UserIDFromCtx(r.Context())
		if uid != 7 {
			http.Error(w, "wrong uid", http.StatusInternalServerError)
			return
		}
		w.WriteHeader(200)
	})

	wrapped := mw.AuthMiddleware(authSvc)(handler)
	req := httptest.NewRequest("GET", "/", nil)
	req.Header.Set("Authorization", "Bearer "+token)
	w := httptest.NewRecorder()
	wrapped.ServeHTTP(w, req)
	if w.Code != 200 {
		t.Fatalf("expected 200 got %d body:%s", w.Code, w.Body.String())
	}
}
