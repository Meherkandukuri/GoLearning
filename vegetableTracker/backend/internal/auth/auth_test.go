package auth

import (
	"testing"
)

func TestHashAndCheckPassword(t *testing.T) {
	s := NewService("test-secret")
	hash, err := s.HashPassword("password123")
	if err != nil {
		t.Fatalf("hash err: %v", err)
	}
	if !s.CheckPassword(hash, "password123") {
		t.Fatalf("password check failed")
	}
}

func TestTokenCreateParse(t *testing.T) {
	s := NewService("another-secret")
	tok, err := s.NewToken(42)
	if err != nil {
		t.Fatalf("new token err: %v", err)
	}
	claims, err := s.ParseToken(tok)
	if err != nil {
		t.Fatalf("parse token err: %v", err)
	}
	if claims.UserID != 42 {
		t.Fatalf("expected user id 42 got %d", claims.UserID)
	}
}
