package models

import (
	"errors"
	"strings"
	"time"
)

// Core domain models

type User struct {
	ID        int64     `db:"id" json:"id"`
	Email     string    `db:"email" json:"email"`
	Password  string    `db:"password_hash" json:"-"`
	CreatedAt time.Time `db:"created_at" json:"created_at"`
}

type Vegetable struct {
	ID          int64      `db:"id" json:"id"`
	Name        string     `db:"name" json:"name"`
	Unit        string     `db:"unit" json:"unit"`
	Category    *string    `db:"category" json:"category,omitempty"`
	LatestPrice *float64   `db:"latest_price" json:"latest_price,omitempty"`
	LastUpdated *time.Time `db:"last_updated" json:"last_updated,omitempty"`
	CreatedAt   time.Time  `db:"created_at" json:"created_at"`
}

type PriceEntry struct {
	ID          int64     `db:"id" json:"id"`
	VegetableID int64     `db:"vegetable_id" json:"vegetable_id"`
	Price       float64   `db:"price" json:"price"`
	Currency    string    `db:"currency" json:"currency"`
	Date        time.Time `db:"date" json:"date"`
	Market      *string   `db:"market" json:"market,omitempty"`
	Notes       *string   `db:"notes" json:"notes,omitempty"`
	CreatedAt   time.Time `db:"created_at" json:"created_at"`
}

type AlertDirection string

const (
	AlertAbove AlertDirection = "above"
	AlertBelow AlertDirection = "below"
)

type Alert struct {
	ID          int64          `db:"id" json:"id"`
	UserID      int64          `db:"user_id" json:"user_id"`
	VegetableID int64          `db:"vegetable_id" json:"vegetable_id"`
	Threshold   float64        `db:"threshold" json:"threshold"`
	Direction   AlertDirection `db:"direction" json:"direction"`
	Active      bool           `db:"active" json:"active"`
	CreatedAt   time.Time      `db:"created_at" json:"created_at"`
	TriggeredAt *time.Time     `db:"triggered_at" json:"triggered_at,omitempty"`
}

// Validation helpers (basic for now)

func ValidateEmail(e string) error {
	if !strings.Contains(e, "@") || len(e) < 6 {
		return errors.New("invalid email")
	}
	return nil
}

func ValidatePassword(p string) error {
	if len(p) < 8 {
		return errors.New("password too short")
	}
	return nil
}

func (v *Vegetable) Validate() error {
	if strings.TrimSpace(v.Name) == "" {
		return errors.New("name required")
	}
	if v.Unit == "" {
		return errors.New("unit required")
	}
	return nil
}

func (p *PriceEntry) Validate() error {
	if p.Price <= 0 {
		return errors.New("price must be positive")
	}
	if p.Currency == "" {
		return errors.New("currency required")
	}
	return nil
}

func (a *Alert) Validate() error {
	if a.Threshold <= 0 {
		return errors.New("threshold must be positive")
	}
	if a.Direction != AlertAbove && a.Direction != AlertBelow {
		return errors.New("invalid direction")
	}
	return nil
}
