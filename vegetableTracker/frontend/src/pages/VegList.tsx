import { useEffect, useState } from 'react'
import api from '../api'
import { useAuth } from '../hooks/useAuth'
import { Link } from 'react-router-dom'

export default function VegList(){
  const [vegs, setVegs] = useState<any[]>([])
  const [name, setName] = useState('')
  const [unit, setUnit] = useState('kg')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')
  const { token } = useAuth()

  const load = ()=> api.get('/vegetables').then((r:any)=>setVegs(r.data)).catch(()=>{})

  useEffect(()=>{ load() },[])

  // auto-clear messages after 3s
  useEffect(()=>{
    if(!msg && !err) return
    const t = setTimeout(()=>{ setMsg(''); setErr('') }, 3000)
    return ()=> clearTimeout(t)
  },[msg, err])

  const create = async (e: any)=>{
    e.preventDefault()
    if(!name.trim()){
      setMsg('Name is required')
      return
    }
    try{
      await api.post('/vegetables', { name: name.trim(), unit })
      setName('')
      setMsg('Created')
      setErr('')
      load()
    }catch(err:any){ console.error(err); setErr(err?.response?.data || 'create failed') }
  }

  const del = async (id: number)=>{
    if(!confirm('Delete this vegetable?')) return
    try{
      await api.delete(`/vegetables/${id}`)
      load()
    }catch(e){ console.error(e) }
  }

  return (
    <div className="card card--padded">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <h2 style={{ margin: 0 }}>Vegetables</h2>
        <div className="small muted">{vegs.length} items</div>
      </div>

      {token && (
        <form onSubmit={create} className="form-inline" style={{ marginBottom: 14 }}>
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
          <input placeholder="Unit (kg, lb...)" value={unit} onChange={e=>setUnit(e.target.value)} />
          <button type="submit" className="btn btn--primary">Create</button>
        </form>
      )}

      {msg && <div className="toast toast-success" style={{ marginBottom: 12 }}>{msg}</div>}
      {err && <div className="toast toast-error" style={{ marginBottom: 12 }}>{err}</div>}

      <ul>
        {vegs.map((v:any)=> (
          <li key={v.id}>
            <div>
              <div className="veg-name"><Link to={`/vegetables/${v.id}`}>{v.name}</Link></div>
              <div className="small muted">Unit: {v.unit || 'kg'}</div>
              <div className="small">{v.latest_price ? `Latest: ${v.latest_price}` : 'No price yet'}</div>
            </div>
            <div className="actions">
              {token && <button className="btn btn--secondary" onClick={()=>del(v.id)}>Delete</button>}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
