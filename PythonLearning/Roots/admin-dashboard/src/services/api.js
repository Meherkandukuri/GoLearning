import axios from "axios";

const API_BASE_URL = "/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("admin_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("admin_token");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Products API
export const productsApi = {
  getAll: () => api.get("/catalog"),
  getById: (id) => api.get(`/catalog/${id}`),
  create: (data) => api.post("/catalog", data),
  update: (id, data) => api.put(`/catalog/${id}`, data),
  delete: (id) => api.delete(`/catalog/${id}`),
};

// Orders API
export const ordersApi = {
  getAll: () => api.get("/orders"),
  getById: (id) => api.get(`/orders/${id}`),
  create: (data) => api.post("/orders", data),
  update: (id, data) => api.put(`/orders/${id}`, data),
  delete: (id) => api.delete(`/orders/${id}`),
};

// WhatsApp API
export const whatsappApi = {
  sendMessage: (data) => api.post("/whatsapp/send", data),
  getWebhookStatus: () => api.get("/whatsapp/webhook/status"),
};

// Health API
export const healthApi = {
  check: () => api.get("/health"),
};

// Auth API
export const authApi = {
  login: (credentials) => api.post("/auth/login", credentials),
  verifyToken: () => api.get("/auth/verify"),
  logout: () => api.post("/auth/logout"),
};

export default api;
