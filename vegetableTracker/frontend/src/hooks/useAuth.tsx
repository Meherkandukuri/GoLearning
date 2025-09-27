import { useState, createContext, useContext, ReactNode, useMemo } from 'react'
import api from '../api'
import { useNavigate } from 'react-router-dom'

type AuthContextValue = {
  token: string | null
  login: (email:string, password:string)=>Promise<void>
  signup: (email:string, password:string)=>Promise<void>
  logout: ()=>void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }){
  const [token, setToken] = useState<string | null>(localStorage.getItem('vt_token'))
  const nav = useNavigate()

  const login = async (email:string, password:string)=>{
    try {
      const res = await api.post('/auth/login', { email, password })
      const t = res.data.token
      localStorage.setItem('vt_token', t)
      setToken(t)
    } catch (err:any) {
      // Normalize error: throw a proper Error with JSON in message so UI can parse
      const server = err?.response?.data || err?.message || 'login failed'
      const e = new Error(typeof server === 'string' ? server : JSON.stringify(server))
      ;(e as any).status = err?.response?.status || 0
      throw e
    }
  }

  const signup = async (email:string, password:string)=>{
    try {
      const res = await api.post('/auth/signup', { email, password })
      const t = res.data.token
      localStorage.setItem('vt_token', t)
      setToken(t)
    } catch (err:any) {
      const server = err?.response?.data || err?.message || 'signup failed'
      const e = new Error(typeof server === 'string' ? server : JSON.stringify(server))
      ;(e as any).status = err?.response?.status || 0
      throw e
    }
  }

  const logout = ()=>{
    localStorage.removeItem('vt_token')
    setToken(null)
    nav('/login')
  }

  const value = useMemo(() => ({ token, login, signup, logout }), [token])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(){
  const ctx = useContext(AuthContext)
  if(!ctx) throw new Error('useAuth must be used inside AuthProvider')
  return ctx
}
