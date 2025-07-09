import React from 'react'
import { Sidebar } from './Sidebar'
import { DashboardHeader } from './DashboardHeader'
import { StatsCards } from './StatsCards'
import { FinanceChart } from './FinanceChart'
import { TasksList } from './TasksList'
import { ActiveTrips } from './ActiveTrips'

interface DashboardProps {
  user?: {
    id: number
    username: string
    first_name: string
    last_name: string
    role: 'ADMIN' | 'DRIVER' | 'MANAGER'
  }
}

export function Dashboard({ user }: DashboardProps) {
  // Пример данных пользователя
  const currentUser = user || {
    id: 1,
    username: 'admin',
    first_name: 'Администратор',
    last_name: 'Системы',
    role: 'ADMIN' as const
  }

  return (
    <div className="w-full h-screen flex bg-background overflow-hidden">
      {/* Боковая панель */}
      <Sidebar 
        isOpen={false} 
        onToggle={() => {}}
        userRole={currentUser.role}
      />

      {/* Основной контент */}
      <div className="ml-64 flex-1 h-screen bg-background overflow-y-auto">
        {/* Верхняя панель */}
        <DashboardHeader 
          user={currentUser}
          onMenuClick={() => {}}
        />

        {/* Основной контент дашборда */}
        <div className="w-full bg-background">
          {/* Карточки статистики */}
          <StatsCards userRole={currentUser.role} />

          {/* Финансы и задачи для не-водителей */}
          {currentUser.role !== 'DRIVER' && (
            <div className="w-full px-8 pt-4 flex justify-start items-start gap-4">
              {/* Финансовая отчетность */}
              <div className="w-2/3">
                <FinanceChart />
              </div>

              {/* Задачи */}
              <div className="w-1/3">
                <TasksList userRole={currentUser.role} />
              </div>
            </div>
          )}
          
          {/* Задачи для водителей на всю ширину */}
          {currentUser.role === 'DRIVER' && (
            <div className="w-full px-8 pt-4">
              <TasksList userRole={currentUser.role} fullWidth />
            </div>
          )}
          
          {/* Активные поездки с картой */}
          <div className="w-full px-8 pt-4 pb-8">
            <ActiveTrips />
          </div>
        </div>
      </div>
    </div>
  )
} 