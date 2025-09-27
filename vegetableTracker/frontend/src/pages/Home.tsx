import React, { useState, useEffect } from 'react'
import EntryForm from '../components/EntryForm'
import EntryTable from '../components/EntryTable'
import EntryCard from '../components/EntryCard'
import Modal from '../components/Modal'
import api from '../api'
import { useAuth } from '../hooks/useAuth'

export default function Home(){
  const { token } = useAuth()
  const [entries, setEntries] = useState<any[]>([])
  const [editing, setEditing] = useState<any | null>(null)
  const [showEditModal, setShowEditModal] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)
  const [err, setErr] = useState<string | null>(null)

  // helper to show temporary messages
  const showTemp = (setter: (v:string|null)=>void, value:string) => { setter(value); setTimeout(()=>setter(null), 3500) }

  // localStorage keys
  const LS_KEY = 'vt_local_entries'

  // load local entries on mount
  useEffect(()=>{
    try{
      const raw = localStorage.getItem(LS_KEY)
      if(raw){
        const parsed = JSON.parse(raw)
        if(Array.isArray(parsed)) setEntries(parsed)
      }
    }catch(e){ /* ignore */ }
  }, [])

  // persist local entries whenever they change (only local-only entries)
  useEffect(()=>{
    try{
      localStorage.setItem(LS_KEY, JSON.stringify(entries))
    }catch(e){ /* ignore */ }
  }, [entries])

  // when token becomes available, attempt to sync local entries that don't have priceId
  useEffect(()=>{
    if(!token) return
    const sync = async ()=>{
      const local = entries.filter(e => !e.priceId)
      if(local.length === 0) return
      for(const e of local){
        try{
          const q = encodeURIComponent(e.name)
          const res = await api.get(`/vegetables?q=${q}`)
          let veg: any = null
          if(Array.isArray(res.data) && res.data.length > 0){
            veg = res.data.find((v:any)=> v.name.toLowerCase() === e.name.toLowerCase()) || res.data[0]
          }
          if(!veg){
            const createRes = await api.post('/vegetables', { name: e.name, unit: e.unit || 'kg' })
            veg = createRes.data
          }
          const priceRes = await api.post(`/vegetables/${veg.id}/prices`, { price: e.price, date: e.date, currency: e.currency || 'USD', market: e.market || '' })
          const price = priceRes.data
          // update entry with persisted ids
          setEntries(prev => prev.map(x => x.id === e.id ? { ...x, vegId: veg.id, priceId: price.id, unit: e.unit || veg.unit || 'kg' } : x))
          showTemp(setMsg, `Synced ${e.name}`)
        }catch(err:any){ console.error('sync failed', err); showTemp(setErr, err?.message || 'sync failed') }
      }
    }
    sync()
  }, [token])

  // load server vegetables when logged in (latest prices)
  const loadServer = async ()=>{
    if(!token) return
    try{
      const res = await api.get('/vegetables')
      if(Array.isArray(res.data)){
        // create entries from server vegetables showing latest_price
  const serverEntries = res.data.map((v:any)=> ({ id: `s-${v.id}`, vegId: v.id, name: v.name, price: v.latest_price || 0, date: v.last_updated ? v.last_updated : new Date().toISOString().slice(0,10), priceId: null, unit: v.unit || 'kg' }))
        // merge server entries with local ones (local-first)
        setEntries(prev => {
          const localOnly = prev.filter(e=> !String(e.id).startsWith('s-'))
          return [...localOnly, ...serverEntries]
        })
      }
    }catch(e){ console.error('load server failed', e) }
  }

  useEffect(()=>{ if(token) loadServer() }, [token])

  const add = async (data:any) => {
    // if not authenticated, store locally
    if(!token){
      const id = Date.now()
      setEntries(prev => [{ id, ...data, unit: data.unit || 'kg' }, ...prev])
      showTemp(setMsg, 'Saved locally (login to persist)')
      return
    }

    try{
      // find vegetable by name
      const q = encodeURIComponent(data.name)
      const res = await api.get(`/vegetables?q=${q}`)
      let veg: any = null
      if(Array.isArray(res.data) && res.data.length > 0){
        // try exact match ignoring case
        veg = res.data.find((v:any)=> v.name.toLowerCase() === data.name.toLowerCase()) || res.data[0]
      }
      if(!veg){
        // create vegetable
        const createRes = await api.post('/vegetables', { name: data.name, unit: data.unit || 'kg' })
        veg = createRes.data
      }
      // add price
      const priceRes = await api.post(`/vegetables/${veg.id}/prices`, { price: data.price, date: data.date, currency: data.currency || 'USD', market: data.market || '' })
      const price = priceRes.data
  const entry = { id: Date.now(), vegId: veg.id, priceId: price.id, name: veg.name, price: price.price, date: price.date, unit: data.unit || veg.unit || 'kg' }
      setEntries(prev => [entry, ...prev])
      showTemp(setMsg, 'Saved to server')
    }catch(e:any){
      console.error('save failed', e)
      showTemp(setErr, e?.response?.data || e.message || 'save failed')
    }
  }

  const onEdit = (entry:any) => { setEditing(entry); setShowEditModal(true) }
  const onDelete = async (entry:any) => {
    // if persisted price id exists, call backend
    if(entry.priceId && token){
      try{
        await api.delete(`/prices/${entry.priceId}`)
        setEntries(prev => prev.filter(e=>e.id !== entry.id))
        showTemp(setMsg, 'Deleted on server')
        return
      }catch(e:any){ console.error(e); showTemp(setErr, e?.response?.data || e.message || 'delete failed'); return }
    }
    // else local-only
    setEntries(prev => prev.filter(e=>e.id !== entry.id))
    showTemp(setMsg, 'Removed locally')
  }

  const saveEdit = async (data:any) => {
    if(editing?.priceId && token){
      try{
        await api.put(`/prices/${editing.priceId}`, { price: data.price, currency: data.currency || 'USD', date: data.date, market: data.market || '' })
        setEntries(prev => prev.map(e => e.id === editing.id ? { ...e, ...data } : e))
        showTemp(setMsg, 'Updated on server')
      }catch(e:any){ console.error(e); showTemp(setErr, e?.response?.data || e.message || 'update failed') }
    }else{
      // local only
      setEntries(prev => prev.map(e => e.id === editing.id ? { ...e, ...data } : e))
      showTemp(setMsg, 'Updated locally')
    }
    setShowEditModal(false); setEditing(null)
  }

  return (
    <div style={{ display: 'grid', gap: 16 }}>
      <EntryForm onSubmit={add} />

      {msg && <div className="toast toast-success">{msg}</div>}
      {err && <div className="toast toast-error">{err}</div>}

      <div style={{ display: 'grid', gap: 12 }}>
        {entries.length === 0 ? (
          <div className="card card--padded">No entries yet — add your first vegetable and price.</div>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            <div className="small muted">Recent entries</div>
            <div className="card" style={{ display: 'grid', gap: 12 }}>
              {entries.map(e => <EntryCard key={e.id} entry={e} onEdit={onEdit} onDelete={onDelete} />)}
            </div>
            <EntryTable entries={entries} onEdit={onEdit} onDelete={onDelete} />
          </div>
        )}
      </div>

      <Modal open={showEditModal} onClose={()=>setShowEditModal(false)}>
        {editing && (
          <div style={{ display: 'grid', gap: 12 }}>
            <h3>Edit entry</h3>
            <EntryForm initial={editing} onSubmit={saveEdit} />
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
              <button className="btn btn--secondary" onClick={()=>setShowEditModal(false)}>Cancel</button>
            </div>
          </div>
        )}
      </Modal>
    </div>
  )
}
