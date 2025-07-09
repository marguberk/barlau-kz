import React, { useState } from 'react'
import { CheckSquare, Plus, Clock, MoreHorizontal } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'

interface Task {
  id: string
  title: string
  description: string
  status: 'NEW' | 'IN_PROGRESS' | 'COMPLETED'
  priority: 'LOW' | 'MEDIUM' | 'HIGH'
  dueDate?: string
  assignedTo?: string
}

interface TasksListProps {
  userRole?: 'ADMIN' | 'DRIVER' | 'MANAGER'
  fullWidth?: boolean
}

export function TasksList({ userRole, fullWidth = false }: TasksListProps) {
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: '1',
      title: 'Проверить состояние грузовика №45',
      description: 'Провести полную диагностику технического состояния автомобиля перед рейсом',
      status: 'NEW',
      priority: 'HIGH',
      dueDate: '2024-12-23',
      assignedTo: 'Иван С.'
    },
    {
      id: '2',
      title: 'Подготовить отчет по расходам',
      description: 'Собрать данные о расходах на топливо за неделю',
      status: 'IN_PROGRESS',
      priority: 'MEDIUM',
      dueDate: '2024-12-24',
      assignedTo: 'Мария К.'
    },
    {
      id: '3',
      title: 'Обновить маршрут доставки',
      description: 'Оптимизировать маршрут с учетом новых адресов',
      status: 'COMPLETED',
      priority: 'LOW',
      dueDate: '2024-12-22',
      assignedTo: 'Алексей П.'
    }
  ])

  const toggleTaskStatus = (taskId: string) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, status: task.status === 'COMPLETED' ? 'NEW' : 'COMPLETED' }
        : task
    ))
  }

  const getPriorityVariant = (priority: string): "default" | "secondary" | "destructive" | "outline" => {
    switch (priority) {
      case 'HIGH':
        return 'destructive'
      case 'MEDIUM':
        return 'default'
      default:
        return 'secondary'
    }
  }

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return 'Срочно'
      case 'MEDIUM':
        return 'Средний'
      default:
        return 'Обычный'
    }
  }

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Без срока'
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', { 
      day: 'numeric', 
      month: 'short', 
      year: 'numeric' 
    })
  }

  const title = userRole === 'DRIVER' ? 'Мои задачи' : 'Задачи'

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <CheckSquare className="h-5 w-5" />
              {title}
            </CardTitle>
            <CardDescription>
              {userRole === 'DRIVER' 
                ? 'Ваши назначенные задачи' 
                : 'Управление задачами команды'
              }
            </CardDescription>
          </div>
          {userRole !== 'DRIVER' && (
            <Button size="sm" variant="outline">
              <Plus className="h-4 w-4 mr-2" />
              Добавить
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent>
        {tasks.length > 0 ? (
          <div className="space-y-4">
            {tasks.map((task) => (
              <div 
                key={task.id}
                className="flex items-start space-x-4 p-3 rounded-lg border bg-card hover:bg-accent/50 transition-colors"
              >
                {/* Чекбокс */}
                <button 
                  onClick={() => toggleTaskStatus(task.id)}
                  className="mt-1"
                >
                  <div className={`flex h-4 w-4 items-center justify-center rounded-sm border border-primary transition-colors ${
                    task.status === 'COMPLETED' 
                      ? 'bg-primary text-primary-foreground' 
                      : 'bg-background hover:bg-accent'
                  }`}>
                    {task.status === 'COMPLETED' && (
                      <CheckSquare className="h-3 w-3" />
                    )}
                  </div>
                </button>

                {/* Содержимое задачи */}
                <div className="flex-1 space-y-2">
                  <div className="space-y-1">
                    <p className={`text-sm font-medium leading-none ${
                      task.status === 'COMPLETED' 
                        ? 'line-through text-muted-foreground' 
                        : ''
                    }`}>
                      {task.title}
                    </p>
                    <p className={`text-sm text-muted-foreground ${
                      task.status === 'COMPLETED' 
                        ? 'line-through' 
                        : ''
                    }`}>
                      {task.description.length > 80 
                        ? `${task.description.substring(0, 80)}...` 
                        : task.description
                      }
                    </p>
                  </div>

                {/* Метаданные */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 text-xs text-muted-foreground">
                    <Clock className="h-3 w-3" />
                    <span>{formatDate(task.dueDate)}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant={getPriorityVariant(task.priority)} className="text-xs">
                      {getPriorityLabel(task.priority)}
                    </Badge>
                    {task.assignedTo && (
                      <Badge variant="outline" className="text-xs">
                        {task.assignedTo}
                      </Badge>
                    )}
                  </div>
                </div>
              </div>

              {/* Меню действий */}
              <Button variant="ghost" size="sm">
                <MoreHorizontal className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center py-8 text-center">
          <CheckSquare className="h-12 w-12 text-muted-foreground/50 mb-4" />
          <h3 className="text-lg font-semibold mb-2">Нет активных задач</h3>
          <p className="text-sm text-muted-foreground mb-4">
            {userRole === 'DRIVER' 
              ? 'У вас пока нет назначенных задач' 
              : 'Создайте новую задачу для начала работы'
            }
          </p>
          {userRole !== 'DRIVER' && (
            <Button>
              <Plus className="h-4 w-4 mr-2" />
              Создать задачу
            </Button>
          )}
        </div>
      )}
    </CardContent>
  </Card>
)
} 