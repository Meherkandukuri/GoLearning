package handlers

import (
	"bytes"
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"strconv"
	"strings"
	"time"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/middleware"

	"github.com/go-chi/chi/v5"

	"github.com/Meherkandukuri/vegetableTracker/backend/internal/auth"
	"github.com/Meherkandukuri/vegetableTracker/backend/internal/models"
	"github.com/Meherkandukuri/vegetableTracker/backend/internal/store"
)

type Handlers struct {
	store *store.DB
	auth  *auth.Service
}

const (
	ErrBadJSON      = "bad json"
	ErrNotFound     = "not found"
	ErrUnauthorized = "unauthorized"
	ErrInvalidCreds = "invalid credentials"
	DateLayout      = "2006-01-02"
)

func New(s *store.DB, a *auth.Service) *Handlers { return &Handlers{store: s, auth: a} }

func (h *Handlers) Routes() chi.Router {
	r := chi.NewRouter()
	// Auth
	r.Post("/auth/signup", h.signup)
	r.Post("/auth/login", h.login)
	// Public Vegetables
	r.Get("/vegetables", h.listVegetables)
	r.Get("/vegetables/{id}", h.getVegetable)
	r.Get("/vegetables/{id}/prices", h.listPrices)
	r.Get("/vegetables/{id}/export", h.exportCSV)
	// Compare
	r.Post("/compare", h.compare)
	return r
}

// RoutesWithAuth returns routes with protected endpoints wrapped by the provided auth middleware.
func (h *Handlers) RoutesWithAuth(authMW func(http.Handler) http.Handler) chi.Router {
	r := h.Routes()
	// Protected endpoints
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Post("/vegetables", h.createVegetable)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Put("/vegetables/{id}", h.updateVegetable)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Delete("/vegetables/{id}", h.deleteVegetable)

	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Post("/vegetables/{id}/prices", h.addPrice)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Put("/prices/{price_id}", h.updatePrice)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Delete("/prices/{price_id}", h.deletePrice)

	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Post("/alerts", h.createAlert)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Get("/alerts", h.listAlerts)
	r.With(func(next http.Handler) http.Handler { return authMW(next) }).Delete("/alerts/{id}", h.deactivateAlert)
	return r
}

// --- Auth ---

type signupReq struct{ Email, Password string }

type signupResp struct {
	UserID int64  `json:"user_id"`
	Token  string `json:"token"`
}

func (h *Handlers) signup(w http.ResponseWriter, r *http.Request) {
	var req signupReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	if err := models.ValidateEmail(req.Email); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if err := models.ValidatePassword(req.Password); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	pwHash, _ := h.auth.HashPassword(req.Password)
	id, err := h.store.CreateUser(r.Context(), req.Email, pwHash)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	token, _ := h.auth.NewToken(id)
	writeJSON(w, 201, signupResp{UserID: id, Token: token})
}

type loginReq struct{ Email, Password string }

type loginResp struct {
	Token string `json:"token"`
}

func (h *Handlers) login(w http.ResponseWriter, r *http.Request) {
	var req loginReq
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	u, err := h.store.GetUserByEmail(r.Context(), req.Email)
	if err != nil || u == nil {
		http.Error(w, ErrInvalidCreds, http.StatusUnauthorized)
		return
	}
	if !h.auth.CheckPassword(u.Password, req.Password) {
		http.Error(w, ErrInvalidCreds, http.StatusUnauthorized)
		return
	}
	token, _ := h.auth.NewToken(u.ID)
	writeJSON(w, 200, loginResp{Token: token})
}

// --- Vegetables ---

func (h *Handlers) listVegetables(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")
	pageStr := r.URL.Query().Get("page")
	limitStr := r.URL.Query().Get("limit")
	page, _ := strconv.Atoi(pageStr)
	limit, _ := strconv.Atoi(limitStr)
	if page < 1 {
		page = 1
	}
	offset := (page - 1) * limit
	list, err := h.store.ListVegetables(r.Context(), q, limit, offset)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	writeJSON(w, 200, list)
}

func (h *Handlers) createVegetable(w http.ResponseWriter, r *http.Request) {
	var v models.Vegetable
	if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	// default unit if missing
	if strings.TrimSpace(v.Unit) == "" {
		v.Unit = "kg"
	}
	if err := v.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	id, err := h.store.CreateVegetable(r.Context(), &v)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	v.ID = id
	writeJSON(w, 201, v)
}

func (h *Handlers) updateVegetable(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	var v models.Vegetable
	if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	v.ID = id
	// default unit if missing
	if strings.TrimSpace(v.Unit) == "" {
		v.Unit = "kg"
	}
	if err := v.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if err := h.store.UpdateVegetable(r.Context(), &v); err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	writeJSON(w, 200, v)
}

func (h *Handlers) deleteVegetable(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	if err := h.store.DeleteVegetable(r.Context(), id); err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	w.WriteHeader(204)
}

func (h *Handlers) getVegetable(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	v, err := h.store.GetVegetable(r.Context(), id)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	if v == nil {
		http.Error(w, ErrNotFound, http.StatusNotFound)
		return
	}
	writeJSON(w, 200, v)
}

// --- Prices ---

func (h *Handlers) listPrices(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	vegID, _ := strconv.ParseInt(idStr, 10, 64)
	var fromPtr, toPtr *time.Time
	if from := r.URL.Query().Get("from"); from != "" {
		if t, err := time.Parse(DateLayout, from); err == nil {
			fromPtr = &t
		}
	}
	if to := r.URL.Query().Get("to"); to != "" {
		if t, err := time.Parse(DateLayout, to); err == nil {
			toPtr = &t
		}
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	offset, _ := strconv.Atoi(r.URL.Query().Get("offset"))
	list, err := h.store.ListPrices(r.Context(), vegID, fromPtr, toPtr, limit, offset)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	min, max, avg, _ := h.store.AggregatePrices(r.Context(), vegID, fromPtr, toPtr)
	writeJSON(w, 200, map[string]any{"vegetable_id": vegID, "prices": list, "aggregate": map[string]*float64{"min": min, "max": max, "avg": avg}})
}

func (h *Handlers) addPrice(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	vegID, _ := strconv.ParseInt(idStr, 10, 64)
	body, err := io.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "invalid json: "+err.Error(), http.StatusBadRequest)
		return
	}
	if len(body) == 0 {
		http.Error(w, "invalid json: empty body", http.StatusBadRequest)
		return
	}
	p, err := parsePricePayload(body)
	if err != nil {
		log.Printf("addPrice parse error: %v body=%s", err, string(body))
		http.Error(w, "invalid json: "+err.Error(), http.StatusBadRequest)
		return
	}
	p.VegetableID = vegID
	if p.Date.IsZero() {
		p.Date = time.Now()
	}
	if err := p.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	id, err := h.store.InsertPrice(r.Context(), p)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	p.ID = id
	writeJSON(w, 201, p)
}

// parsePricePayload tolerantly parses price (number or string) and date (RFC3339 or YYYY-MM-DD).
func parsePricePayload(body []byte) (*models.PriceEntry, error) {
	type raw struct {
		Price    interface{} `json:"price"`
		Currency string      `json:"currency"`
		Date     *string     `json:"date"`
		Market   *string     `json:"market"`
		Notes    *string     `json:"notes"`
	}
	var in raw
	if err := json.Unmarshal(body, &in); err != nil {
		return nil, err
	}
	var price float64
	switch v := in.Price.(type) {
	case float64:
		price = v
	case string:
		if v == "" {
			return nil, fmt.Errorf("price required")
		}
		p, err := strconv.ParseFloat(v, 64)
		if err != nil {
			return nil, fmt.Errorf("invalid price: %w", err)
		}
		price = p
	case nil:
		return nil, fmt.Errorf("price required")
	default:
		return nil, fmt.Errorf("invalid price type")
	}
	pe := &models.PriceEntry{Price: price, Currency: in.Currency}
	if in.Market != nil && strings.TrimSpace(*in.Market) != "" {
		pe.Market = in.Market
	}
	if in.Notes != nil && strings.TrimSpace(*in.Notes) != "" {
		pe.Notes = in.Notes
	}
	if in.Date != nil && *in.Date != "" {
		if t, err := time.Parse(time.RFC3339, *in.Date); err == nil {
			pe.Date = t
		} else if t2, err2 := time.Parse(DateLayout, *in.Date); err2 == nil {
			pe.Date = t2
		} else {
			return nil, fmt.Errorf("invalid date format")
		}
	}
	return pe, nil
}

func (h *Handlers) updatePrice(w http.ResponseWriter, r *http.Request) {
	priceIDStr := chi.URLParam(r, "price_id")
	pid, _ := strconv.ParseInt(priceIDStr, 10, 64)
	p, err := h.store.GetPriceEntry(r.Context(), pid)
	if err != nil || p == nil {
		http.Error(w, "not found", 404)
		return
	}
	if err := json.NewDecoder(r.Body).Decode(p); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	if err := p.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	if err := h.store.UpdatePriceEntry(r.Context(), p); err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	writeJSON(w, 200, p)
}

func (h *Handlers) deletePrice(w http.ResponseWriter, r *http.Request) {
	priceIDStr := chi.URLParam(r, "price_id")
	pid, _ := strconv.ParseInt(priceIDStr, 10, 64)
	if err := h.store.DeletePriceEntry(r.Context(), pid); err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	w.WriteHeader(204)
}

// --- Compare ---

func (h *Handlers) compare(w http.ResponseWriter, r *http.Request) {
	type req struct {
		VegetableIDs []int64 `json:"vegetable_ids"`
		From, To     string
	}
	var body req
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	// For brevity, reuse ListPrices per vegetable (could batch optimize later)
	resp := make(map[string]any)
	for _, id := range body.VegetableIDs {
		prices, _ := h.store.ListPrices(r.Context(), id, nil, nil, 100, 0)
		resp[strconv.FormatInt(id, 10)] = prices
	}
	writeJSON(w, 200, resp)
}

// --- Export ---

func (h *Handlers) exportCSV(w http.ResponseWriter, r *http.Request) {
	idStr := chi.URLParam(r, "id")
	vegID, _ := strconv.ParseInt(idStr, 10, 64)
	veg, err := h.store.GetVegetable(r.Context(), vegID)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	if veg == nil {
		http.Error(w, ErrNotFound, http.StatusNotFound)
		return
	}
	prices, _ := h.store.ListPrices(r.Context(), vegID, nil, nil, 1000, 0)
	w.Header().Set("Content-Type", "text/csv")
	// build a safe filename: vegetable-{id}-{slug(name)}-{unit}-prices.csv
	slug := func(s string) string {
		// very small slug helper: lowercase, replace spaces with '-', remove problematic chars
		out := ""
		for _, r := range s {
			if r >= 'A' && r <= 'Z' {
				r = r + ('a' - 'A')
			}
			if (r >= 'a' && r <= 'z') || (r >= '0' && r <= '9') || r == '-' {
				out += string(r)
			} else if r == ' ' || r == '_' {
				out += "-"
			}
		}
		if out == "" {
			out = "veg"
		}
		return out
	}
	filename := "vegetable-" + strconv.FormatInt(veg.ID, 10) + "-" + slug(veg.Name) + "-" + slug(veg.Unit) + "-prices.csv"
	w.Header().Set("Content-Disposition", "attachment; filename="+filename)
	// build CSV in-memory including metadata comments, then write at once
	var buf bytes.Buffer
	fmt.Fprintf(&buf, "# name: %s\n", veg.Name)
	fmt.Fprintf(&buf, "# unit: %s\n", veg.Unit)
	cw := csv.NewWriter(&buf)
	// include unit in header and rows
	_ = cw.Write([]string{"id", "date", "price", "currency", "market", "notes", "unit"})
	for _, p := range prices {
		cw.Write([]string{strconv.FormatInt(p.ID, 10), p.Date.Format(DateLayout), strconv.FormatFloat(p.Price, 'f', 2, 64), p.Currency, deref(p.Market), deref(p.Notes), veg.Unit})
	}
	cw.Flush()
	// set headers and write the complete buffer to response
	w.Header().Set("Content-Type", "text/csv")
	w.Header().Set("Content-Disposition", "attachment; filename="+filename)
	w.Write(buf.Bytes())
}

// --- Alerts ---

func (h *Handlers) createAlert(w http.ResponseWriter, r *http.Request) {
	var a models.Alert
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, ErrBadJSON, http.StatusBadRequest)
		return
	}
	if err := a.Validate(); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	id, err := h.store.CreateAlert(r.Context(), &a)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	a.ID = id
	writeJSON(w, 201, a)
}

func (h *Handlers) listAlerts(w http.ResponseWriter, r *http.Request) {
	uid := userIDFromCtx(r.Context())
	if uid == 0 {
		http.Error(w, ErrUnauthorized, http.StatusUnauthorized)
		return
	}
	alerts, err := h.store.ListAlerts(r.Context(), uid)
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	writeJSON(w, 200, alerts)
}

func (h *Handlers) deactivateAlert(w http.ResponseWriter, r *http.Request) {
	uid := userIDFromCtx(r.Context())
	if uid == 0 {
		http.Error(w, "unauthorized", 401)
		return
	}
	idStr := chi.URLParam(r, "id")
	id, _ := strconv.ParseInt(idStr, 10, 64)
	if err := h.store.DeactivateAlert(r.Context(), id, uid); err != nil {
		http.Error(w, ErrNotFound, http.StatusNotFound)
		return
	}
	w.WriteHeader(204)
}

// --- Helpers ---

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func deref(s *string) string {
	if s == nil {
		return ""
	}
	return *s
}

// userIDFromCtx is a thin wrapper around the middleware helper to avoid
// changing handler code everywhere.
func userIDFromCtx(ctx context.Context) int64 {
	return middleware.UserIDFromCtx(ctx)
}
