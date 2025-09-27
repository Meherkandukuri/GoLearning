import React, { useState, useEffect } from 'react'
import api from '../api'

let debounceTimer: any = null

export default function EntryForm({ onSubmit, initial }: any){
  const [name, setName] = useState(initial?.name || '')
  const [price, setPrice] = useState(initial?.price ? String(initial.price) : '')
  const [date, setDate] = useState(initial?.date ? initial.date.slice(0,10) : new Date().toISOString().slice(0,10))
  const [suggestions, setSuggestions] = useState<any[]>([])
  const [unit, setUnit] = useState(initial?.unit || 'kg')

  useEffect(()=>{
    if(!name) { setSuggestions([]); return }
    if(debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(async ()=>{
      try{
        const q = encodeURIComponent(name)
        const res = await api.get(`/vegetables?q=${q}`)
        const list = Array.isArray(res.data) ? res.data.slice(0,6) : []
        setSuggestions(list)
      }catch(e){ setSuggestions([]) }
    }, 300)
    return ()=>{ if(debounceTimer) clearTimeout(debounceTimer) }
  }, [name])

  const submit = (e:any) => {
    e.preventDefault()
    if(!name.trim()) return
    onSubmit({ name: name.trim(), price: parseFloat(price), date, unit })
  }

  return (
    <form onSubmit={submit} className="card card--padded" style={{ display: 'grid', gap: 12 }}>
      <label>
        Vegetable name
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="e.g., Tomato" autoComplete="off" />
        {suggestions.length > 0 && (
          <div style={{ marginTop: 8, display: 'grid', gap: 6 }}>
                {suggestions.map(s => (
                  <button key={s.id} type="button" className="btn btn--secondary" onClick={()=>{ setName(s.name); if(s.unit) setUnit(s.unit); setSuggestions([]) }} style={{ justifyContent: 'flex-start' }}>{s.name}{s.unit ? ` — ${s.unit}` : ''}</button>
                ))}
          </div>
        )}
      </label>
      <div style={{ display: 'flex', gap: 12 }}>
        <label style={{ flex: 1 }}>
          Price
          <input value={price} onChange={e=>setPrice(e.target.value)} placeholder="e.g., 12.50" type="number" step="0.01" />
        </label>
        <label style={{ width: 180 }}>
          Date
          <input type="date" value={date} onChange={e=>setDate(e.target.value)} />
        </label>
      </div>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            <label style={{ display: 'flex', flexDirection: 'column' }}>
              Unit
              <select value={unit} onChange={e=>setUnit(e.target.value)} style={{ padding: '8px 10px', borderRadius: 8 }}>
                <option value="kg">kg</option>
                <option value="g">g</option>
                <option value="lb">lb</option>
                <option value="bunch">bunch</option>
                <option value="litre">litre</option>
                <option value="piece">piece</option>
              </select>
            </label>
          </div>
      <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
        <button type="submit" className="btn btn--primary">Add</button>
      </div>
    </form>
  )
}
