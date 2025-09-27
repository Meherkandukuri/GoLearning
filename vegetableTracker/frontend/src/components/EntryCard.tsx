import React from 'react'

export default function EntryCard({ entry, onEdit, onDelete }: any){
  return (
    <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
      <div>
        <div className="veg-name">{entry.name}</div>
  <div className="small muted">{new Date(entry.date).toLocaleDateString()} · {entry.price}{entry.unit ? ` / ${entry.unit}` : ''}</div>
      </div>
      <div className="actions">
        <button className="btn btn--secondary" onClick={()=>onEdit(entry)}>Edit</button>
        <button className="btn btn--danger" onClick={()=>onDelete(entry)}>Delete</button>
      </div>
    </div>
  )
}
