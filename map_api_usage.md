# Анализ использования API для карты

## Архитектура API взаимодействия

### Серверная часть
Серверная часть API для карты реализована через Django REST Framework с следующими компонентами:

1. **MapViewSet** - основной ViewSet для обработки запросов карты:
   - Наследуется от `viewsets.ViewSet`
   - Имеет методы для получения данных и обновления местоположения
   - Поддерживает работу с анонимными и авторизованными пользователями

2. **URL маршруты**:
   ```python
   router.register(r'map', MapViewSet, basename='map')
   
   urlpatterns = [
       path('', include(router.urls)),
       path('map/live_tracking/', MapViewSet.as_view({'get': 'get_vehicles'}), name='live-tracking'),
       path('map/update_location/', MapViewSet.as_view({'post': 'update_location'}), name='update-location'),
       path('map/tracking_status/', MapViewSet.as_view({'post': 'update_tracking_status'}), name='tracking-status'),
   ]
   ```

3. **Модели данных**:
   - `Vehicle` - информация о транспортных средствах
   - `Task` - информация о задачах, связанных с транспортом
   - `User` - информация о пользователях (включая водителей)

### Клиентская часть
Клиентская часть реализована с использованием JavaScript и библиотеки Leaflet:

1. **Инициализация карты**:
   ```javascript
   const map = L.map('map').setView([43.238949, 76.889709], 13);
   L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
       attribution: '&copy; OpenStreetMap contributors'
   }).addTo(map);
   ```

2. **Хранение данных**:
   ```javascript
   let vehicleMarkers = {};  // Объект для хранения маркеров транспорта
   ```

## Процесс обмена данными

### Получение данных о транспорте
**Запрос:**
```javascript
function loadVehicles() {
    console.log('Загружаем транспортные средства');
    
    // Очищаем существующие маркеры
    clearVehicleMarkers();
    
    // В реальной системе был бы запрос к API:
    // fetch('/api/v1/map/?token=' + new Date().getTime(), {
    //    headers: {'Authorization': 'Bearer ' + tokenValue}
    // })
    // .then(response => response.json())
    // .then(data => {
    //     displayVehicles(data.vehicles);
    //     updateCounters(data.vehicles);
    // });
    
    // В демо-режиме используем тестовые данные
    displayVehicles(demoVehicles);
    updateCounters(demoVehicles);
    updateLastUpdateTime();
}
```

**Ответ API (пример):**
```json
{
  "vehicles": [
    {
      "id": 1,
      "number": "KZ 123 ABC",
      "brand": "Toyota",
      "model": "Camry",
      "driver_name": "Иван Иванов",
      "latitude": 43.2517,
      "longitude": 76.9186,
      "last_update": "2023-12-01T14:30:00Z"
    },
    ...
  ],
  "isDriverMode": false
}
```

### Обновление местоположения транспортного средства
**Запрос:**
```javascript
function updateVehicleLocation(latitude, longitude) {
    fetch('/api/v1/map/update_location/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + tokenValue
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Местоположение обновлено');
    });
}
```

**Ответ API (пример):**
```json
{
  "id": 1,
  "number": "KZ 123 ABC",
  "brand": "Toyota",
  "model": "Camry",
  "driver_name": "Иван Иванов",
  "latitude": 43.2517,
  "longitude": 76.9186,
  "last_update": "2023-12-01T14:35:00Z"
}
```

### Обновление статуса отслеживания
**Запрос:**
```javascript
function updateTrackingStatus(enabled) {
    fetch('/api/v1/map/tracking_status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + tokenValue
        },
        body: JSON.stringify({
            tracking_enabled: enabled
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Статус отслеживания обновлен');
    });
}
```

**Ответ API (пример):**
```json
{
  "tracking_enabled": true,
  "message": "Статус отслеживания успешно обновлен"
}
```

## Обработка данных на клиенте

### Отображение транспортных средств
```javascript
function displayVehicles(vehicles) {
    console.log('Отображаем транспортные средства:', vehicles);
    
    vehicles.forEach(function(vehicle) {
        var latlng = [
            vehicle.driver.current_latitude,
            vehicle.driver.current_longitude
        ];
        
        // Определяем цвет в зависимости от статуса
        var iconColor;
        var isActive = vehicle.status === 'active' && vehicle.speed > 0;
        var isLongStopped = vehicle.lastUpdate && (new Date().getTime() - vehicle.lastUpdate > 60 * 60 * 1000);
        
        if (isActive) {
            iconColor = '#2563EB'; // Синий - активен в движении
        } else if (isLongStopped) {
            iconColor = '#EF4444'; // Красный - долгий простой
        } else {
            iconColor = '#6B7280'; // Серый - на стоянке
        }
        
        // Создаем маркер и добавляем его на карту
        var vehicleIcon = L.divIcon({
            className: isActive ? 'vehicle-marker active-marker' : 'vehicle-marker',
            html: '<i class="fas fa-truck" style="color: ' + iconColor + '"></i>',
            iconSize: [30, 30],
            iconAnchor: [15, 15]
        });
        
        var marker = L.marker(latlng, {icon: vehicleIcon}).addTo(map);
        
        // Добавляем всплывающее окно
        marker.bindPopup(
            '<div class="p-2">' +
            '<h3 class="text-lg font-semibold mb-2">' + vehicle.brand + ' ' + vehicle.model + '</h3>' +
            '<p class="text-sm mb-1"><strong>Гос. номер:</strong> ' + vehicle.number + '</p>' +
            '<p class="text-sm mb-1"><strong>Водитель:</strong> ' + vehicle.driver.fullname + '</p>' +
            '<p class="text-sm mb-1"><strong>Телефон:</strong> ' + vehicle.driver.phone + '</p>' +
            '<p class="text-sm mb-1"><strong>Скорость:</strong> ' + vehicle.speed + ' км/ч</p>' +
            '<p class="text-sm"><strong>Последнее обновление:</strong> ' + lastUpdateText + '</p>' +
            '</div>'
        );
        
        // Сохраняем маркер
        vehicleMarkers[vehicle.id] = marker;
    });
}
```

### Обновление счетчиков
```javascript
function updateCounters(vehicles) {
    var total = vehicles.length;
    var active = vehicles.filter(v => v.status === 'active' && v.speed > 0).length;
    var stopped = total - active;
    
    document.getElementById('totalVehicles').textContent = total;
    document.getElementById('activeVehicles').textContent = active;
    document.getElementById('stoppedVehicles').textContent = stopped;
}
```

## Особенности и ограничения API

### Демонстрационный режим
Для неавторизованных пользователей или в демонстрационных целях API возвращает тестовые данные:

```python
def get_vehicles(self, request):
    # Проверяем, аутентифицирован ли пользователь
    if not request.user.is_authenticated:
        # Для неавторизованных пользователей возвращаем демо-данные
        demo_data = {
            'vehicles': [
                {
                    'id': 1,
                    'number': 'KZ 123 ABC',
                    'driver': {
                        'fullname': 'Демонстрационный водитель 1',
                        'current_latitude': 43.2517,
                        'current_longitude': 76.9186
                    },
                    'type': 'car',
                    'status': 'active'
                },
                # ... другие демо-транспортные средства
            ],
            'isDriverMode': False
        }
        return Response(demo_data)
```

### Разграничение прав доступа
API учитывает роли пользователей и предоставляет разный уровень доступа:

1. **Неавторизованные пользователи** - получают только демо-данные
2. **Водители** - могут видеть только свои транспортные средства и обновлять свое местоположение
3. **Диспетчеры и администраторы** - видят все транспортные средства и задачи

```python
# Фильтруем транспортные средства в зависимости от роли пользователя
if is_driver:
    vehicles = vehicles.filter(driver=request.user)
```

### Периодическое обновление
Клиентский код настроен на автоматическое обновление данных каждые 5 минут:

```javascript
// Запускаем автоматическое обновление каждые 5 минут
setInterval(loadVehicles, 5 * 60 * 1000);
```

### Обработка ошибок
В клиентском коде реализована обработка ошибок при получении данных (не показано в демо-примере, но должно быть реализовано в полной версии):

```javascript
fetch('/api/v1/map/')
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка сети или сервера');
        }
        return response.json();
    })
    .then(data => {
        displayVehicles(data.vehicles);
        updateCounters(data.vehicles);
    })
    .catch(error => {
        console.error('Ошибка загрузки данных:', error);
        // Показать сообщение об ошибке пользователю
    });
``` 