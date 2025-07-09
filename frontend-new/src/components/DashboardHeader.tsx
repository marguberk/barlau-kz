import React, { useState } from 'react'
import { Bell, User } from 'lucide-react'

interface DashboardHeaderProps {
  user: {
    id: number
    username: string
    first_name: string
    last_name: string
    role: 'ADMIN' | 'DRIVER' | 'MANAGER'
  }
  onMenuClick: () => void
}

export function DashboardHeader({ user, onMenuClick }: DashboardHeaderProps) {
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [notificationCount] = useState(3) // Пример количества уведомлений

  return (
    <div className="w-full h-20 px-8 py-5 bg-card flex justify-between items-center border-b">
      <div className="justify-start text-foreground text-2xl font-semibold leading-loose">
        Дашборд
      </div>

      <div className="flex justify-start items-center gap-3">
        {/* Уведомления */}
        <div className="flex justify-start items-start gap-2">
          <button className="w-10 h-10 px-3 py-2 bg-card rounded-lg shadow-sm border flex justify-center items-center gap-1.5 relative hover:bg-accent transition-colors">
            <Bell className="w-5 h-5" />
            {notificationCount > 0 && (
              <span className="absolute -top-2 -right-2 bg-destructive rounded-full border-2 border-background flex items-center justify-center font-bold shadow-lg transition-all duration-200 text-destructive-foreground text-xs min-w-[1.4rem] min-h-[1.4rem]">
                {notificationCount}
              </span>
            )}
          </button>
        </div>

        {/* Меню пользователя */}
        <div className="flex justify-start items-center gap-1.5 relative">
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center gap-2 p-1 rounded-lg hover:bg-accent transition-colors"
            >
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                <span className="text-xs font-semibold text-primary-foreground">
                  {user.first_name.charAt(0)}{user.last_name.charAt(0)}
                </span>
              </div>
            </button>

            {/* Выпадающее меню */}
            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-44 bg-card border rounded-lg shadow-lg z-50">
                <button className="block w-full text-left px-4 py-2 text-foreground hover:bg-accent rounded-t-lg">
                  Профиль
                </button>
                <button className="block w-full text-left px-4 py-2 text-foreground hover:bg-accent rounded-b-lg">
                  Выйти
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
} 