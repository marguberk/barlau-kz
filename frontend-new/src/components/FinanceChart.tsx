import React, { useState } from 'react'
import { ChevronDown, TrendingUp } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'

export function FinanceChart() {
  const [selectedPeriod, setSelectedPeriod] = useState('Месяц')
  const [selectedYear, setSelectedYear] = useState('2024')

  // Пример финансовых данных
  const income = 152250
  const expenses = 86520
  const incomeGrowth = 12.05
  const expensesGrowth = 8.25

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Финансовая отчетность</CardTitle>
            <CardDescription>
              Обзор доходов и расходов за выбранный период
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              {selectedPeriod}
              <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
            <Button variant="outline" size="sm">
              {selectedYear}
              <ChevronDown className="ml-2 h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {/* Показатели */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2 mb-6">
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">Доход</p>
            <div className="flex items-baseline space-x-2">
              <p className="text-2xl font-bold text-green-600">
                {income.toLocaleString('ru-RU')}₸
              </p>
              <div className="flex items-center text-sm text-green-600">
                <TrendingUp className="mr-1 h-3 w-3" />
                +{incomeGrowth}%
              </div>
            </div>
          </div>
          <div className="space-y-2">
            <p className="text-sm font-medium text-muted-foreground">Расход</p>
            <div className="flex items-baseline space-x-2">
              <p className="text-2xl font-bold text-red-600">
                {expenses.toLocaleString('ru-RU')}₸
              </p>
              <div className="flex items-center text-sm text-red-600">
                <TrendingUp className="mr-1 h-3 w-3" />
                +{expensesGrowth}%
              </div>
            </div>
          </div>
        </div>

        {/* График */}
        <div className="h-[200px] w-full">
          <svg width="100%" height="100%" viewBox="0 0 600 200" className="overflow-visible">
            {/* Сетка */}
            <defs>
              <pattern id="grid" width="60" height="40" patternUnits="userSpaceOnUse">
                <path d="M 60 0 L 0 0 0 40" fill="none" stroke="hsl(var(--border))" strokeWidth="0.5"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
            
            {/* График прошлого месяца */}
            <path 
              d="M0,120 C50,100 100,140 150,130 C200,120 250,110 300,100 C350,90 400,100 450,90 C500,80 550,85 600,75" 
              stroke="hsl(var(--muted-foreground))" 
              strokeWidth="2" 
              fill="none" 
              opacity="0.6"
            />
            
            {/* График текущего месяца */}
            <path 
              d="M0,140 C50,120 100,130 150,110 C200,90 250,100 300,80 C350,70 400,80 450,70 C500,65 550,60 600,50" 
              stroke="hsl(var(--primary))" 
              strokeWidth="2" 
              fill="none" 
            />
            
            {/* Точки на графике */}
            {[
              { x: 0, y: 140 }, { x: 150, y: 110 }, { x: 300, y: 80 }, 
              { x: 450, y: 70 }, { x: 600, y: 50 }
            ].map((point, index) => (
              <circle 
                key={index}
                cx={point.x} 
                cy={point.y} 
                r="3" 
                fill="hsl(var(--primary))"
                className="hover:r-4 cursor-pointer transition-all"
              />
            ))}
          </svg>
        </div>

        {/* Итоговая информация */}
        <div className="flex items-center justify-between pt-4 border-t">
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Чистая прибыль</p>
            <p className="text-lg font-semibold">
              {(income - expenses).toLocaleString('ru-RU')}₸
            </p>
          </div>
          <div className="flex items-center space-x-4 text-xs">
            <div className="flex items-center space-x-1">
              <div className="h-2 w-2 rounded-full bg-primary"></div>
              <span className="text-muted-foreground">Текущий месяц</span>
            </div>
            <div className="flex items-center space-x-1">
              <div className="h-2 w-2 rounded-full bg-muted-foreground"></div>
              <span className="text-muted-foreground">Прошлый месяц</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 