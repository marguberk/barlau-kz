import React, { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Eye, EyeOff, Loader2 } from 'lucide-react'

interface LoginFormProps {
  onSubmit: (username: string, password: string) => void
  isLoading?: boolean
}

export function LoginForm({ onSubmit, isLoading = false }: LoginFormProps) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(username, password)
  }

  return (
    <>
      {/* Адаптивные стили для фонового изображения */}
      <style>{`
        .bg-dots-adaptive {
          background-image: url(/images/bg-dots.png);
          background-position: center;
          background-color: #f8fafc;
          
          /* Десктоп - уменьшенный размер для лучшего вида */
          background-repeat: no-repeat;
          background-size: 60%;
        }
        
        /* Планшеты - начинаем повторение */
        @media (max-width: 1024px) {
          .bg-dots-adaptive {
            background-repeat: repeat;
            background-size: 400px 400px;
          }
        }
        
        /* Мобильные устройства - повторение как в оригинале */
        @media (max-width: 768px) {
          .bg-dots-adaptive {
            background-repeat: repeat;
            background-size: 300px 300px;
          }
        }
        
        /* Маленькие мобильные - мелкое повторение */
        @media (max-width: 480px) {
          .bg-dots-adaptive {
            background-repeat: repeat;
            background-size: 250px 250px;
          }
        }
      `}</style>
      
      <div className="min-h-screen font-['Inter_Tight'] relative bg-dots-adaptive">
        {/* Логотип в самом верху - менее жирный */}
        <div className="pt-8 pb-4 flex justify-center animate-in fade-in-0 slide-in-from-top-4 duration-1000">
          <div className="flex items-center space-x-3">
            <img 
              src="/images/logo.png" 
              alt="Barlau Logo" 
              className="w-[42px] h-[23px]" 
            />
            <h1 className="text-2xl md:text-3xl font-semibold text-foreground">Barlau.kz</h1>
          </div>
        </div>
        
        {/* Форма по центру экрана - уменьшенная ширина */}
        <div className="flex items-center justify-center px-4" style={{ minHeight: 'calc(100vh - 120px)' }}>
          <Card className="w-full max-w-sm shadow-2xl border-0 animate-in fade-in-0 slide-in-from-bottom-4 duration-1000 delay-200">
            <CardHeader className="space-y-1 text-center pb-6">
              <CardTitle className="text-xl md:text-2xl font-semibold">Войдите в систему</CardTitle>
              <CardDescription className="text-xs md:text-sm text-muted-foreground">
                Введите номер телефона и пароль для доступа
              </CardDescription>
            </CardHeader>
            
            <CardContent className="pb-8">
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Поле телефона с заголовком */}
                <div className="space-y-2">
                  <Label htmlFor="username" className="text-sm font-medium">
                    Номер телефона
                  </Label>
                  <Input
                    id="username"
                    type="text"
                    placeholder="+7 ___ ___ __ __"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    disabled={isLoading}
                    className="h-12 bg-muted/50 border-border focus:bg-background transition-colors text-base"
                  />
                </div>

                {/* Поле пароля с заголовком */}
                <div className="space-y-2">
                  <Label htmlFor="password" className="text-sm font-medium">
                    Пароль
                  </Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Введите пароль"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      disabled={isLoading}
                      className="h-12 pr-10 transition-colors text-base"
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                      disabled={isLoading}
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4 text-muted-foreground" />
                      ) : (
                        <Eye className="h-4 w-4 text-muted-foreground" />
                      )}
                    </Button>
                  </div>
                </div>

                {/* Кнопка входа - принудительно синий цвет */}
                <Button
                  type="submit"
                  className="w-full h-12 font-semibold text-base mt-6 bg-[#2679DB] hover:bg-[#1e5fa3] text-white"
                  disabled={isLoading || !username || !password}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Вход...
                    </>
                  ) : (
                    'Войти'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    </>
  )
} 