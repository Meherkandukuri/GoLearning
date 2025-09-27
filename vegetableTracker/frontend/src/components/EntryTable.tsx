import React from 'react'

export default function EntryTable({ entries, onEdit, onDelete }: any){
  return (
    <div className="card card--padded">
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
            <tr style={{ textAlign: 'left', color: 'var(--muted)' }}>
            <th style={{ padding: '8px 6px' }}>Name</th>
            <th style={{ padding: '8px 6px' }}>Date</th>
            <th style={{ padding: '8px 6px' }}>Price</th>
            <th style={{ padding: '8px 6px' }}>Unit</th>
            <th style={{ padding: '8px 6px', textAlign: 'right' }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((e:any)=> (
            <tr key={e.id} style={{ borderTop: '1px solid rgba(15,23,36,0.04)' }}>
              <td style={{ padding: '10px 6px' }}>{e.name}</td>
              <td style={{ padding: '10px 6px' }}>{new Date(e.date).toLocaleDateString()}</td>
              <td style={{ padding: '10px 6px' }}>{e.price}</td>
              <td style={{ padding: '10px 6px' }}>{e.unit || ''}</td>
              <td style={{ padding: '10px 6px', textAlign: 'right' }}>
                <button className="btn btn--secondary" onClick={()=>onEdit(e)} style={{ marginRight: 8 }}>Edit</button>
                <button className="btn btn--danger" onClick={()=>onDelete(e)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
