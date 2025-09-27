import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import api from '../api'

export default function VegDetail(){
  const { id } = useParams<{id: string}>()
  const [veg, setVeg] = useState<any>(null)
  const [prices, setPrices] = useState<any[]>([])
  const [priceVal, setPriceVal] = useState('')
  const [currency, setCurrency] = useState('USD')
  const [market, setMarket] = useState('')
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')

  useEffect(()=>{
    if(!id) return
    api.get(`/vegetables/${id}`).then(r=>setVeg(r.data)).catch(()=>{})
    api.get(`/vegetables/${id}/prices`).then(r=>setPrices(r.data.prices || r.data)).catch(()=>{})
  },[id])

  const addPrice = async (e:any) => {
    e.preventDefault()
    if(!id) return
    if(!priceVal) { setErr('Price required'); return }
    const parsed = parseFloat(priceVal)
    if(Number.isNaN(parsed) || parsed <= 0) { setErr('Price must be a positive number'); return }
    try{
      await api.post(`/vegetables/${id}/prices`, { price: parsed, currency, market, date: new Date().toISOString() })
      setPriceVal('')
      setMarket('')
      setCurrency('USD')
      api.get(`/vegetables/${id}/prices`).then((r:any)=>setPrices(r.data.prices || r.data))
      api.get(`/vegetables/${id}`).then((r:any)=>setVeg(r.data))
      setMsg('Added')
      setErr('')
    }catch(e){ console.error(e) }
  }

  const downloadCSV = async ()=>{
    try{
      const res = await api.get(`/vegetables/${id}/export`, { responseType: 'blob' })
      const blob = new Blob([res.data], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      // try to get filename from Content-Disposition header
      const cd = res.headers && (res.headers['content-disposition'] || res.headers['Content-Disposition'])
      if(cd){
        const m = cd.match(/filename=("?)([^";]+)/i)
        if(m && m[2]) a.download = m[2]
      }
      if(!a.download){
        const safe = (s:string)=> s ? s.toLowerCase().replace(/[^a-z0-9]+/g,'-') : 'veg'
        a.download = `vegetable-${id}-${safe(veg?.name||'')}-${safe(veg?.unit||'kg')}-prices.csv`
      }
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    }catch(e){
      console.error('download failed', e)
    }
  }

  // auto-clear messages
  useEffect(()=>{
    if(!msg && !err) return
    const t = setTimeout(()=>{ setMsg(''); setErr('') }, 3000)
    return ()=> clearTimeout(t)
  },[msg, err])

  if(!veg) return <div className="card card--padded">Loading...</div>

  return (
    <div className="card card--padded">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12, marginBottom: 12 }}>
        <div>
          <h2 style={{ margin: 0 }}>{veg.name}</h2>
          <div className="small muted">{veg.description || ''}</div>
          <div className="small muted">Unit: {veg.unit || 'kg'}</div>
        </div>
        <div className="small">{veg.latest_price ? `Latest: ${veg.latest_price}` : 'No price yet'}</div>
      </div>

      <div style={{ marginBottom: 14 }}>
        <button className="btn btn--secondary" onClick={downloadCSV}>Download CSV</button>
      </div>

      <h3 style={{ marginTop: 8 }}>Prices</h3>
      <form onSubmit={addPrice} className="form-inline" style={{ marginBottom: 12 }}>
        <input placeholder="Price" value={priceVal} onChange={e=>setPriceVal(e.target.value)} />
        <input placeholder="Currency" value={currency} onChange={e=>setCurrency(e.target.value)} />
        <input placeholder="Market" value={market} onChange={e=>setMarket(e.target.value)} />
        <button type="submit" className="btn btn--primary">Add Price</button>
      </form>

      {msg && <div className="toast toast-success" style={{ marginBottom: 12 }}>{msg}</div>}
      {err && <div className="toast toast-error" style={{ marginBottom: 12 }}>{err}</div>}

      <ul>
        {prices.map((p:any) => (
          <li key={p.id}>
            <div>
              <div className="small">{p.date}</div>
              <div className="veg-name">{p.price} {p.currency} {p.market ? `(${p.market})` : ''}</div>
            </div>
            <div className="actions">
              <button className="btn btn--danger" onClick={async ()=>{
                if(!confirm('Delete this price?')) return
                try{ await api.delete(`/prices/${p.id}`); api.get(`/vegetables/${id}/prices`).then((r:any)=>setPrices(r.data.prices || r.data)) }catch(e){ console.error(e) }
              }}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
