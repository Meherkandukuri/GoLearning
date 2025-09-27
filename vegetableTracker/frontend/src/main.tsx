import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import App from './App'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Home from './pages/Home'
import VegList from './pages/VegList'
import VegDetail from './pages/VegDetail'
import './styles.css'
import { AuthProvider } from './hooks/useAuth'
import { setNavigateToLogin } from './api'
import { useNavigate } from 'react-router-dom'
import RequireAuth from './hooks/RequireAuth'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        {/* wire api 401 -> login redirect */}
        <InitRedirect />
        <Routes>
          <Route path='/' element={<App/>}>
            <Route index element={<Home/>} />
            <Route path='vegetables' element={<RequireAuth><VegList/></RequireAuth>} />
            <Route path='vegetables/:id' element={<RequireAuth><VegDetail/></RequireAuth>} />
            <Route path='login' element={<Login/>} />
            <Route path='signup' element={<Signup />} />
          </Route>
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
)

function InitRedirect(){
  const nav = useNavigate()
  React.useEffect(()=>{ setNavigateToLogin(()=>()=>nav('/login')) },[nav])
  return null
}
