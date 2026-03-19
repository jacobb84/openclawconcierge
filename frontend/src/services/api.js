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

export const pluginsService = {
  getAll: () => api.get('/plugins'),
  getDashboard: () => api.get('/plugins/dashboard'),
  reload: (name) => api.post(`/plugins/${name}/reload`),
  updateConfig: (name, config) => api.put(`/plugins/${name}/config`, config),
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
  getAll: (params) => api.get('/careers/companies', { params }),
  getOne: (id) => api.get(`/careers/companies/${id}`),
  update: (id, data) => api.put(`/careers/companies/${id}`, data),
  delete: (id) => api.delete(`/careers/companies/${id}`),
};

export const jobsService = {
  getAll: (params) => api.get('/careers/jobs', { params }),
  getOne: (id) => api.get(`/careers/jobs/${id}`),
  update: (id, data) => api.put(`/careers/jobs/${id}`, data),
  delete: (id) => api.delete(`/careers/jobs/${id}`),
};

export const apiKeysService = {
  getAll: () => api.get('/api-keys'),
  getOne: (id) => api.get(`/api-keys/${id}`),
  create: (data) => api.post('/api-keys', data),
  update: (id, data) => api.put(`/api-keys/${id}`, data),
  delete: (id) => api.delete(`/api-keys/${id}`),
  regenerate: (id) => api.post(`/api-keys/${id}/regenerate`),
};

export default api;
