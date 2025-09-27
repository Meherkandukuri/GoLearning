-- 001_init.sql: initial schema
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vegetables (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    unit TEXT NOT NULL,
    category TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS price_entries (
    id BIGSERIAL PRIMARY KEY,
    vegetable_id BIGINT NOT NULL REFERENCES vegetables(id) ON DELETE CASCADE,
    price NUMERIC(12,2) NOT NULL,
    currency TEXT NOT NULL,
    date DATE NOT NULL,
    market TEXT NULL,
    notes TEXT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_price_entries_veg_date ON price_entries(vegetable_id, date DESC);

CREATE TABLE IF NOT EXISTS alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    vegetable_id BIGINT NOT NULL REFERENCES vegetables(id) ON DELETE CASCADE,
    threshold NUMERIC(12,2) NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('above','below')),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    triggered_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_user_active ON alerts(user_id, active);