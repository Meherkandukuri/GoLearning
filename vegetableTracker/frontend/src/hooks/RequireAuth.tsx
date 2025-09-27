import { Navigate } from 'react-router-dom'
import { useAuth } from './useAuth'

export default function RequireAuth({ children }: { children: JSX.Element }){
  const { token } = useAuth()
  if(!token) return <Navigate to="/login" replace />
  return children
}
