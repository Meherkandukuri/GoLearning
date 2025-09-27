import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function Login(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  const { login } = useAuth()
  const nav = useNavigate()

  const submit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await login(email, password)
      setMsg('Logged in')
      nav('/')
    } catch (err:any){
      const server = err?.response?.data
      setMsg(server || err?.message || 'error')
    }
  }

  return (
    <div className="card auth-card card--padded">
      <h2 style={{ marginTop: 0 }}>Login</h2>
      <form onSubmit={submit} className="form">
        <label>Email<input value={email} onChange={e=>setEmail(e.target.value)} /></label>
        <label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>
        <div className="form-inline">
          <button type="submit" className="btn btn--primary">Login</button>
          <button type="button" className="btn btn--secondary" onClick={()=>window.location.href='/signup'}>Create account</button>
        </div>
  {msg && <div className="small muted" style={{ marginTop: 8 }}>{typeof msg === 'string' ? msg : JSON.stringify(msg)}</div>}
      </form>
    </div>
  )
}
