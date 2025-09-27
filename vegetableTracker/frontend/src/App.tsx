import { Outlet, Link } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'

export default function App(){
  const { token, logout } = useAuth()
  return (
    <div className="app">
      <header>
        <h1>Vegetable Price Tracker</h1>
        <nav>
          <Link to="/">Home</Link> |
          {token ? (
            <button onClick={logout} style={{ marginLeft: 8 }}>Logout</button>
          ) : (
            <><Link to="/login">Login</Link> | <Link to="/signup">Signup</Link></>
          )}
        </nav>
      </header>
      <main>
        <Outlet />
      </main>
    </div>
  )
}
