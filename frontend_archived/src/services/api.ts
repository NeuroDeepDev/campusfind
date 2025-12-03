import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/token/refresh/`, {
            refresh: refreshToken,
          })
          const { access } = response.data
          localStorage.setItem('access_token', access)
          api.defaults.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (err) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

// API calls
export const authApi = {
  register: (data: any) => api.post('/users/students/register/', data),
  login: (username: string, password: string) =>
    api.post('/token/', { username, password }),
  refreshToken: (refresh: string) =>
    api.post('/token/refresh/', { refresh }),
  getCurrentUser: () => api.get('/users/students/me/'),
  verifyEmail: (data: any) => api.post('/auth/users/activation/', data),
  resetPassword: (email: string) =>
    api.post('/auth/users/reset_password/', { email }),
}

export const itemsApi = {
  list: (params?: any) => api.get('/items/', { params }),
  get: (id: number) => api.get(`/items/${id}/`),
  create: (data: FormData) =>
    api.post('/items/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  update: (id: number, data: any) => api.patch(`/items/${id}/`, data),
  foundItems: () => api.get('/items/found_items/'),
  lostItems: () => api.get('/items/lost_items/'),
  myItems: () => api.get('/items/my_items/'),
}

export const claimsApi = {
  list: (params?: any) => api.get('/claims/', { params }),
  get: (id: number) => api.get(`/claims/${id}/`),
  create: (data: FormData) =>
    api.post('/claims/', data, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  myClaims: () => api.get('/claims/my_claims/'),
  pending: () => api.get('/claims/pending/'),
  approve: (id: number) => api.post(`/claims/${id}/approve/`),
  reject: (id: number) => api.post(`/claims/${id}/reject/`),
}

export const reportsApi = {
  list: (params?: any) => api.get('/reports/', { params }),
  get: (id: number) => api.get(`/reports/${id}/`),
  create: (data: any) => api.post('/reports/', data),
  myReports: () => api.get('/reports/my_reports/'),
}

export const auditApi = {
  list: (params?: any) => api.get('/audit/', { params }),
  byAction: (action: string) =>
    api.get('/audit/by_action/', { params: { action } }),
  claimHistory: (claimId: number) =>
    api.get('/audit/claim_history/', { params: { claim_id: claimId } }),
}

export const categoriesApi = {
  list: () => api.get('/categories/'),
}

export const locationsApi = {
  list: () => api.get('/locations/'),
}
