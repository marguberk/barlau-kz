import React from 'react'
import { Home, CheckSquare, MapPin, Truck, Users } from 'lucide-react'

interface SidebarProps {
  isOpen: boolean
  onToggle: () => void
  userRole?: 'ADMIN' | 'DRIVER' | 'MANAGER'
}

export function Sidebar({ isOpen, onToggle, userRole }: SidebarProps) {
  const menuItems = [
    { id: 'home', label: 'Главная', icon: Home, active: true },
    { id: 'tasks', label: 'Задачи', icon: CheckSquare },
    { id: 'map', label: 'Карта', icon: MapPin },
    ...(userRole !== 'DRIVER' ? [
      { id: 'trucks', label: 'Грузовики', icon: Truck },
      { id: 'employees', label: 'Сотрудники', icon: Users }
    ] : [])
  ]

  return (
    <div className="w-64 h-screen bg-card border-r flex flex-col justify-start items-start fixed left-0 bottom-0">
      {/* Логотип */}
      <div className="self-stretch px-5 py-6 relative flex flex-col justify-start items-start gap-2">
        <div className="py-1 inline-flex justify-start items-center gap-2">
          <img 
            src="/images/logo.png" 
            alt="Barlau Logo" 
            className="w-10 h-6" 
          />
          <div className="text-center justify-start text-foreground text-2xl font-semibold leading-normal">
            Barlau.kz
          </div>
        </div>
      </div>

      {/* Меню навигации */}
      <div className="self-stretch flex-1 px-4 pt-2 pb-4 flex flex-col justify-start items-center gap-4">
        <div className="self-stretch flex flex-col justify-start items-start gap-1">
          <div className="self-stretch flex flex-col justify-start items-start">
            {menuItems.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.id}
                  className={`self-stretch px-3 py-3.5 rounded-lg inline-flex items-center gap-2 relative transition-colors ${
                    item.active 
                      ? 'bg-accent text-primary' 
                      : 'bg-transparent text-muted-foreground hover:bg-accent hover:text-foreground'
                  }`}
                >
                  {item.active && (
                    <div className="w-1 h-6 left-0 top-[calc(50%-12px)] absolute bg-primary rounded-tr-lg rounded-br-lg" />
                  )}
                  <Icon className="w-5 h-5" />
                  <div className="flex-1 text-base font-medium leading-normal tracking-tight text-left">
                    {item.label}
                  </div>
                </button>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
} 