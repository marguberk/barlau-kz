import React from 'react'
import { CheckSquare, Bell, Truck } from 'lucide-react'

interface StatsCardsProps {
  userRole?: 'ADMIN' | 'DRIVER' | 'MANAGER'
}

export function StatsCards({ userRole }: StatsCardsProps) {
  // Пример данных
  const tasksCount = 5
  const notificationsCount = 3
  const activeTripsCount = 8

  return (
    <div className="w-full px-8 pt-4 flex justify-start items-start gap-4">
      {/* Задачи на сегодня */}
      <div className="flex-1 px-5 py-6 bg-card rounded-2xl shadow-sm border flex flex-col justify-start items-start gap-4 overflow-hidden">
        <div className="self-stretch flex flex-col justify-start items-start gap-2">
          <div className="self-stretch inline-flex justify-between items-center">
            <div className="justify-start text-foreground text-4xl font-semibold leading-10">
              {tasksCount}
            </div>
            <div className="w-10 h-10 p-2 bg-primary rounded-lg shadow-sm flex justify-center items-center gap-2 overflow-hidden">
              <CheckSquare className="w-5 h-5 text-primary-foreground" />
            </div>
          </div>
          <div className="self-stretch justify-start text-muted-foreground text-base font-normal leading-normal">
            Задач на сегодня
          </div>
        </div>
      </div>

      {/* Вторая карточка - разная для водителей и менеджеров */}
      {userRole === 'DRIVER' ? (
        // Уведомления для водителей
        <div className="flex-1 px-5 py-6 bg-card rounded-2xl shadow-sm border flex flex-col justify-start items-start gap-4 overflow-hidden">
          <div className="self-stretch flex flex-col justify-start items-start gap-2">
            <div className="self-stretch inline-flex justify-between items-center">
              <div className="justify-start text-foreground text-4xl font-semibold leading-10">
                {notificationsCount}
              </div>
              <div className="w-10 h-10 p-2 bg-primary rounded-lg shadow-sm flex justify-center items-center gap-2 overflow-hidden">
                <Bell className="w-5 h-5 text-primary-foreground" />
              </div>
            </div>
            <div className="self-stretch justify-start text-muted-foreground text-base font-normal leading-normal">
              Уведомления
            </div>
          </div>
        </div>
      ) : (
        // Активные поездки для менеджеров
        <div className="flex-1 px-5 py-6 bg-card rounded-2xl shadow-sm border flex flex-col justify-start items-start gap-4 overflow-hidden">
          <div className="self-stretch flex flex-col justify-start items-start gap-2">
            <div className="self-stretch inline-flex justify-between items-center">
              <div className="justify-start text-foreground text-4xl font-semibold leading-10">
                {activeTripsCount}
              </div>
              <div className="w-10 h-10 p-2 bg-primary rounded-lg shadow-sm flex justify-center items-center gap-2 overflow-hidden">
                <Truck className="w-5 h-5 text-primary-foreground" />
              </div>
            </div>
            <div className="self-stretch justify-start text-muted-foreground text-base font-normal leading-normal">
              Активные поездки
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 