import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import router from '../router'

// 根据环境选择 API 地址
const baseURL = import.meta.env.PROD 
  ? `${import.meta.env.VITE_API_BASE_URL}/api`
  : '/api'

const api = axios.create({
  baseURL,
  withCredentials: true
})

api.interceptors.request.use(config => {
  const auth = useAuthStore()
  if (auth.csrfToken) config.headers['X-CSRF-Token'] = auth.csrfToken
  return config
})

// 响应拦截器：处理 401 错误
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      const auth = useAuthStore()
      auth.setAuthed(false)
      auth.setCsrf('')
      localStorage.clear()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export default api