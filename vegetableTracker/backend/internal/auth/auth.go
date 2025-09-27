package auth

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

type Service struct {
	secret []byte
	ttl    time.Duration
}

func NewService(secret string) *Service {
	return &Service{secret: []byte(secret), ttl: 24 * time.Hour}
}

func (s *Service) HashPassword(pw string) (string, error) {
	b, err := bcrypt.GenerateFromPassword([]byte(pw), bcrypt.DefaultCost)
	return string(b), err
}

func (s *Service) CheckPassword(hash, pw string) bool {
	return bcrypt.CompareHashAndPassword([]byte(hash), []byte(pw)) == nil
}

type Claims struct {
	UserID int64 `json:"user_id"`
	jwt.RegisteredClaims
}

func (s *Service) NewToken(userID int64) (string, error) {
	c := Claims{UserID: userID, RegisteredClaims: jwt.RegisteredClaims{ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.ttl)), IssuedAt: jwt.NewNumericDate(time.Now())}}
	t := jwt.NewWithClaims(jwt.SigningMethodHS256, c)
	return t.SignedString(s.secret)
}

func (s *Service) ParseToken(tokenStr string) (*Claims, error) {
	parsed, err := jwt.ParseWithClaims(tokenStr, &Claims{}, func(t *jwt.Token) (interface{}, error) { return s.secret, nil })
	if err != nil {
		return nil, err
	}
	c, ok := parsed.Claims.(*Claims)
	if !ok || !parsed.Valid {
		return nil, errors.New("invalid token")
	}
	return c, nil
}
