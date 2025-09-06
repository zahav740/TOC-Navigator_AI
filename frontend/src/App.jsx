import React, { useState } from 'react'
import Login from './components/Login'
import Orders from './components/Orders'

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false)

  return loggedIn ? (
    <Orders />
  ) : (
    <Login onLogin={() => setLoggedIn(true)} />
  )
}
