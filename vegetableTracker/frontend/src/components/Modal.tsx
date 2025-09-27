import React from 'react'

export default function Modal({ open, onClose, children }: any){
  if(!open) return null
  const onKey = (e:any) => { if(e.key === 'Escape') onClose() }
  return (
    <div style={{ position: 'fixed', inset:0, display:'flex', alignItems:'center', justifyContent:'center', zIndex:60 }} onKeyDown={onKey}>
      <button aria-label="close modal" onClick={onClose} style={{ position:'absolute', inset:0, border:0, background:'rgba(12,12,12,0.35)', padding:0, cursor:'default' }} />
      <div className="card" role="dialog" aria-modal="true" tabIndex={0} style={{ zIndex:70, minWidth: 320, maxWidth: '90%', padding: 18 }}>
        {children}
      </div>
    </div>
  )
}
