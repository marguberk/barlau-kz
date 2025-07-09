import React, { useState } from 'react'
import './App.css'
import { LoginForm } from './components/LoginForm'
import { Dashboard } from './components/Dashboard'

function App() {
  // Временно включаем автоматический вход для тестирования
  const [isLoggedIn, setIsLoggedIn] = useState(true)
  const [user, setUser] = useState<{
    id: number
    username: string
    first_name: string
    last_name: string
    role: 'ADMIN' | 'DRIVER' | 'MANAGER'
  } | null>({
    id: 1,
    username: 'admin',
    first_name: 'Администратор',
    last_name: 'Системы',
    role: 'ADMIN'
  })

  const handleLogin = (username: string, password: string) => {
    // Симуляция входа
    console.log('Вход:', username, password)
    
    // Пример пользователей
    const mockUsers = {
      'admin': {
        id: 1,
        username: 'admin',
        first_name: 'Администратор',
        last_name: 'Системы',
        role: 'ADMIN' as const
      },
      'driver': {
        id: 2,
        username: 'driver',
        first_name: 'Иван',
        last_name: 'Петров',
        role: 'DRIVER' as const
      },
      'manager': {
        id: 3,
        username: 'manager',
        first_name: 'Мария',
        last_name: 'Сидорова',
        role: 'MANAGER' as const
      }
    }
    
    const mockUser = mockUsers[username as keyof typeof mockUsers] || mockUsers.admin
    
    setUser(mockUser)
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    setUser(null)
    setIsLoggedIn(false)
  }

  if (!isLoggedIn) {
    return <LoginForm onSubmit={handleLogin} />
  }

  return <Dashboard user={user || undefined} />
}

export default App
