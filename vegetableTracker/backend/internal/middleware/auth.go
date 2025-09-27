package middleware

import (
	"context"
	"net/http"
	"strings"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/auth"
)

type ctxKey string

const userIDKey ctxKey = "userID"

func UserIDFromCtx(ctx context.Context) int64 {
	v := ctx.Value(userIDKey)
	if v == nil {
		return 0
	}
	if id, ok := v.(int64); ok {
		return id
	}
	return 0
}

// AuthMiddleware validates the Bearer token and injects the userID into context.
func AuthMiddleware(authSvc *auth.Service) func(http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			authz := r.Header.Get("Authorization")
			if authz == "" || !strings.HasPrefix(authz, "Bearer ") {
				http.Error(w, "unauthorized", http.StatusUnauthorized)
				return
			}
			token := strings.TrimPrefix(authz, "Bearer ")
			claims, err := authSvc.ParseToken(token)
			if err != nil {
				http.Error(w, "unauthorized", http.StatusUnauthorized)
				return
			}
			ctx := context.WithValue(r.Context(), userIDKey, claims.UserID)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}
