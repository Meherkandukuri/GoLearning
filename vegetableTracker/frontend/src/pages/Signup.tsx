import { useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { useNavigate } from 'react-router-dom'

export default function Signup(){
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')
  const { signup } = useAuth()
  const nav = useNavigate()

  const submit = async (e: any) => {
    e.preventDefault()
    try{
      await signup(email, password)
      setMsg('Registered')
      nav('/')
    }catch(err:any){ setErr(err?.response?.data || 'signup failed') }
  }

  return (
    <div className="card auth-card card--padded">
      <h2 style={{ marginTop: 0 }}>Signup</h2>
      <form onSubmit={submit} className="form">
        <label>Email<input value={email} onChange={e=>setEmail(e.target.value)} /></label>
        <label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>
        <div className="form-inline">
          <button type="submit" className="btn btn--primary">Signup</button>
          <button type="button" className="btn btn--secondary" onClick={()=>window.location.href='/login'}>Back to login</button>
        </div>
  {msg && <div className="small muted" style={{ marginTop: 8 }}>{msg}</div>}
  {err && <div className="small" style={{ color: '#ef4444', marginTop: 8 }}>{typeof err === 'string' ? err : JSON.stringify(err)}</div>}
      </form>
    </div>
  )
}
