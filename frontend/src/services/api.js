import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authService = {
  login: (username, password) => api.post('/auth/login', { username, password }),
  me: () => api.get('/auth/me'),
};

export const concertsService = {
  getAll: (params) => api.get('/concerts', { params }),
  getOne: (id) => api.get(`/concerts/${id}`),
  update: (id, data) => api.put(`/concerts/${id}`, data),
  delete: (id) => api.delete(`/concerts/${id}`),
};

export const eventsService = {
  getAll: (params) => api.get('/events', { params }),
  getOne: (id) => api.get(`/events/${id}`),
  update: (id, data) => api.put(`/events/${id}`, data),
  delete: (id) => api.delete(`/events/${id}`),
};

export const newsService = {
  getAll: (params) => api.get('/news', { params }),
  getOne: (id) => api.get(`/news/${id}`),
  update: (id, data) => api.put(`/news/${id}`, data),
  delete: (id) => api.delete(`/news/${id}`),
};

export const companiesService = {
  getAll: (params) => api.get('/career/companies', { params }),
  getOne: (id) => api.get(`/career/companies/${id}`),
  update: (id, data) => api.put(`/career/companies/${id}`, data),
  delete: (id) => api.delete(`/career/companies/${id}`),
};

export const jobsService = {
  getAll: (params) => api.get('/career/jobs', { params }),
  getOne: (id) => api.get(`/career/jobs/${id}`),
  update: (id, data) => api.put(`/career/jobs/${id}`, data),
  delete: (id) => api.delete(`/career/jobs/${id}`),
};

export default api;
