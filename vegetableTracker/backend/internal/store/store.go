package store

import (
	"context"
	"database/sql"
	"errors"
	"fmt"
	"time"

	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/models"
)

type DB struct {
	Conn *sqlx.DB
}

func Open(dsn string) (*DB, error) {
	db, err := sqlx.Open("postgres", dsn)
	if err != nil {
		return nil, err
	}
	if err = db.Ping(); err != nil {
		return nil, err
	}
	return &DB{Conn: db}, nil
}

// User repo

func (db *DB) CreateUser(ctx context.Context, email, passwordHash string) (int64, error) {
	var id int64
	err := db.Conn.QueryRowContext(ctx, `INSERT INTO users (email, password_hash) VALUES ($1,$2) RETURNING id`, email, passwordHash).Scan(&id)
	return id, err
}

func (db *DB) GetUserByEmail(ctx context.Context, email string) (*models.User, error) {
	var u models.User
	err := db.Conn.GetContext(ctx, &u, `SELECT * FROM users WHERE email=$1`, email)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	return &u, err
}

// Vegetables

func (db *DB) CreateVegetable(ctx context.Context, v *models.Vegetable) (int64, error) {
	var id int64
	err := db.Conn.QueryRowContext(ctx, `INSERT INTO vegetables (name, unit, category) VALUES ($1,$2,$3) RETURNING id`, v.Name, v.Unit, v.Category).Scan(&id)
	return id, err
}

func (db *DB) ListVegetables(ctx context.Context, q string, limit, offset int) ([]models.Vegetable, error) {
	if limit == 0 {
		limit = 20
	}
	args := []interface{}{}
	where := ""
	if q != "" {
		where = "WHERE name ILIKE $1"
		args = append(args, "%"+q+"%")
	}
	query := fmt.Sprintf("SELECT v.*, lp.price AS latest_price, lp.created_at AS last_updated FROM vegetables v LEFT JOIN LATERAL (SELECT price, created_at FROM price_entries p WHERE p.vegetable_id=v.id ORDER BY date DESC, id DESC LIMIT 1) lp ON true %s ORDER BY v.name LIMIT %d OFFSET %d", where, limit, offset)
	rows, err := db.Conn.QueryxContext(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []models.Vegetable
	for rows.Next() {
		var v models.Vegetable
		if err := rows.StructScan(&v); err != nil {
			return nil, err
		}
		list = append(list, v)
	}
	return list, rows.Err()
}

func (db *DB) GetVegetable(ctx context.Context, id int64) (*models.Vegetable, error) {
	var v models.Vegetable
	err := db.Conn.GetContext(ctx, &v, `SELECT * FROM vegetables WHERE id=$1`, id)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	return &v, err
}

// Prices

func (db *DB) InsertPrice(ctx context.Context, p *models.PriceEntry) (int64, error) {
	var id int64
	err := db.Conn.QueryRowContext(ctx, `INSERT INTO price_entries (vegetable_id, price, currency, date, market, notes) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id`, p.VegetableID, p.Price, p.Currency, p.Date, p.Market, p.Notes).Scan(&id)
	return id, err
}

func (db *DB) ListPrices(ctx context.Context, vegID int64, from, to *time.Time, limit, offset int) ([]models.PriceEntry, error) {
	if limit == 0 {
		limit = 50
	}
	query := `SELECT * FROM price_entries WHERE vegetable_id=$1`
	args := []interface{}{vegID}
	if from != nil {
		query += fmt.Sprintf(" AND date >= $%d", len(args)+1)
		args = append(args, *from)
	}
	if to != nil {
		query += fmt.Sprintf(" AND date <= $%d", len(args)+1)
		args = append(args, *to)
	}
	query += " ORDER BY date DESC, id DESC LIMIT $" + fmt.Sprint(len(args)+1) + " OFFSET $" + fmt.Sprint(len(args)+2)
	args = append(args, limit, offset)
	var list []models.PriceEntry
	err := db.Conn.SelectContext(ctx, &list, query, args...)
	return list, err
}

func (db *DB) AggregatePrices(ctx context.Context, vegID int64, from, to *time.Time) (min, max, avg *float64, err error) {
	query := `SELECT MIN(price), MAX(price), AVG(price) FROM price_entries WHERE vegetable_id=$1`
	args := []interface{}{vegID}
	if from != nil {
		query += " AND date >= $2"
		args = append(args, *from)
	}
	if to != nil {
		query += " AND date <= $3"
		args = append(args, *to)
	}
	err = db.Conn.QueryRowContext(ctx, query, args...).Scan(&min, &max, &avg)
	return
}

// Alerts

func (db *DB) CreateAlert(ctx context.Context, a *models.Alert) (int64, error) {
	var id int64
	err := db.Conn.QueryRowContext(ctx, `INSERT INTO alerts (user_id, vegetable_id, threshold, direction, active) VALUES ($1,$2,$3,$4,$5) RETURNING id`, a.UserID, a.VegetableID, a.Threshold, a.Direction, a.Active).Scan(&id)
	return id, err
}

func (db *DB) ListAlerts(ctx context.Context, userID int64) ([]models.Alert, error) {
	var list []models.Alert
	err := db.Conn.SelectContext(ctx, &list, `SELECT * FROM alerts WHERE user_id=$1 AND active=true`, userID)
	return list, err
}

// --- Additional CRUD ---

func (db *DB) UpdateVegetable(ctx context.Context, v *models.Vegetable) error {
	_, err := db.Conn.ExecContext(ctx, `UPDATE vegetables SET name=$1, unit=$2, category=$3 WHERE id=$4`, v.Name, v.Unit, v.Category, v.ID)
	return err
}

func (db *DB) DeleteVegetable(ctx context.Context, id int64) error {
	_, err := db.Conn.ExecContext(ctx, `DELETE FROM vegetables WHERE id=$1`, id)
	return err
}

func (db *DB) GetPriceEntry(ctx context.Context, id int64) (*models.PriceEntry, error) {
	var p models.PriceEntry
	err := db.Conn.GetContext(ctx, &p, `SELECT * FROM price_entries WHERE id=$1`, id)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, nil
	}
	return &p, err
}

func (db *DB) UpdatePriceEntry(ctx context.Context, p *models.PriceEntry) error {
	_, err := db.Conn.ExecContext(ctx, `UPDATE price_entries SET price=$1, currency=$2, date=$3, market=$4, notes=$5 WHERE id=$6`, p.Price, p.Currency, p.Date, p.Market, p.Notes, p.ID)
	return err
}

func (db *DB) DeletePriceEntry(ctx context.Context, id int64) error {
	_, err := db.Conn.ExecContext(ctx, `DELETE FROM price_entries WHERE id=$1`, id)
	return err
}

func (db *DB) DeactivateAlert(ctx context.Context, id int64, userID int64) error {
	res, err := db.Conn.ExecContext(ctx, `UPDATE alerts SET active=false WHERE id=$1 AND user_id=$2`, id, userID)
	if err != nil {
		return err
	}
	n, _ := res.RowsAffected()
	if n == 0 {
		return sql.ErrNoRows
	}
	return nil
}
