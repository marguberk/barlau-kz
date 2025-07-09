import React, { useState } from 'react'
import { MapPin, Navigation, Truck, User, Clock, MoreHorizontal } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'

interface Trip {
  id: string
  driver: string
  truck: string
  from: string
  to: string
  status: 'IN_PROGRESS' | 'LOADING' | 'UNLOADING' | 'COMPLETED'
  startTime: string
  estimatedArrival: string
  progress: number
}

export function ActiveTrips() {
  const [activeTrips] = useState<Trip[]>([
    {
      id: '1',
      driver: 'Иван Петров',
      truck: 'КZ 123 AB',
      from: 'Алматы',
      to: 'Астана',
      status: 'IN_PROGRESS',
      startTime: '08:30',
      estimatedArrival: '18:45',
      progress: 65
    },
    {
      id: '2',
      driver: 'Мария Сидорова',
      truck: 'КZ 456 CD',
      from: 'Шымкент',
      to: 'Караганда',
      status: 'LOADING',
      startTime: '09:15',
      estimatedArrival: '16:30',
      progress: 15
    },
    {
      id: '3',
      driver: 'Алексей Козлов',
      truck: 'КZ 789 EF',
      from: 'Актобе',
      to: 'Павлодар',
      status: 'UNLOADING',
      startTime: '07:00',
      estimatedArrival: '15:20',
      progress: 95
    }
  ])

  const getStatusVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case 'IN_PROGRESS':
        return 'default'
      case 'LOADING':
        return 'secondary'
      case 'UNLOADING':
        return 'outline'
      case 'COMPLETED':
        return 'secondary'
      default:
        return 'outline'
    }
  }

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return 'В пути'
      case 'LOADING':
        return 'Загрузка'
      case 'UNLOADING':
        return 'Разгрузка'
      case 'COMPLETED':
        return 'Завершен'
      default:
        return 'Неизвестно'
    }
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <MapPin className="h-5 w-5" />
              Активные поездки
            </CardTitle>
            <CardDescription>
              {activeTrips.length} активных поездок в реальном времени
            </CardDescription>
          </div>
          <Button variant="outline" size="sm">
            Показать все
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-3 lg:grid-cols-3">
          {/* Карта */}
          <div className="md:col-span-2">
            <div className="h-[300px] w-full rounded-lg border bg-muted/50 flex items-center justify-center">
              <div className="text-center space-y-2">
                <MapPin className="h-12 w-12 mx-auto text-muted-foreground" />
                <h3 className="text-lg font-semibold">Карта поездок</h3>
                <p className="text-sm text-muted-foreground">
                  Интерактивная карта с маршрутами в реальном времени
                </p>
              </div>
              
              {/* Анимированные точки */}
              <div className="absolute">
                <div className="relative">
                  <div className="absolute top-4 left-4 w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                  <div className="absolute top-1/2 left-1/3 w-2 h-2 bg-orange-500 rounded-full animate-pulse"></div>
                  <div className="absolute bottom-8 right-8 w-2 h-2 bg-[#2679DB] rounded-full animate-pulse"></div>
                </div>
              </div>
            </div>
          </div>

          {/* Список поездок */}
          <div className="space-y-4">
            {activeTrips.map((trip) => (
              <Card key={trip.id} className="p-4">
                <div className="space-y-3">
                  {/* Водитель и грузовик */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <User className="h-4 w-4 text-muted-foreground" />
                      <span className="text-sm font-medium">{trip.driver}</span>
                    </div>
                    <div className="flex items-center space-x-1">
                      <Truck className="h-3 w-3 text-muted-foreground" />
                      <span className="text-xs text-muted-foreground">{trip.truck}</span>
                    </div>
                  </div>

                  {/* Маршрут */}
                  <div className="flex items-center space-x-2 text-sm">
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                      <span className="text-muted-foreground">{trip.from}</span>
                    </div>
                    <Navigation className="h-3 w-3 text-muted-foreground" />
                    <div className="flex items-center space-x-1">
                      <div className="w-2 h-2 bg-red-500 rounded-full"></div>
                      <span className="text-muted-foreground">{trip.to}</span>
                    </div>
                  </div>

                  {/* Статус и время */}
                  <div className="flex items-center justify-between">
                    <Badge variant={getStatusVariant(trip.status)} className="text-xs">
                      {getStatusLabel(trip.status)}
                    </Badge>
                    <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                      <Clock className="h-3 w-3" />
                      <span>{trip.startTime} - {trip.estimatedArrival}</span>
                    </div>
                  </div>

                  {/* Прогресс */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs">
                      <span className="text-muted-foreground">Прогресс</span>
                      <span className="font-medium">{trip.progress}%</span>
                    </div>
                    <Progress value={trip.progress} className="h-2" />
                  </div>

                  {/* Действия */}
                  <div className="flex justify-end">
                    <Button variant="ghost" size="sm">
                      <MoreHorizontal className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 