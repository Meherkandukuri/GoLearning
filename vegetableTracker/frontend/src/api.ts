import axios from 'axios'

const api = axios.create({
  // backend mounts handlers under /api (see cmd/api/main.go)
  baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8080/api',
})

let navigateToLogin: (()=>void) | null = null
export function setNavigateToLogin(fn: ()=>void){ navigateToLogin = fn }

api.interceptors.request.use(cfg=>{
  const t = localStorage.getItem('vt_token')
  if(t) cfg.headers = { ...(cfg.headers||{}), Authorization: `Bearer ${t}` }
  return cfg
})

api.interceptors.response.use(resp=>resp, err=>{
  if(err?.response?.status === 401){
    localStorage.removeItem('vt_token')
    if(navigateToLogin) navigateToLogin()
  }
  return Promise.reject(err)
})

export default api
