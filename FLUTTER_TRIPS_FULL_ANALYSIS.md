# ДЕТАЛЬНЫЙ АНАЛИЗ FLUTTER ВЕРСИИ ЗАЕЗДОВ

## 🎯 СТРУКТУРА ЭКРАНА ЗАЕЗДОВ (TripsScreen)

### 📱 **Общая структура:**
- **3 вкладки:** "Активные", "Все заезды", "График"
- **TabController** для переключения вкладок
- **Фильтры** на третьей вкладке (дата, водитель, транспорт)

### 📋 **Вкладки (TabBar):**
```dart
tabs: [
  Tab(text: 'Активные'),     // Только ACTIVE статусы
  Tab(text: 'Все заезды'),   // Все поездки
  Tab(text: 'График'),       // С фильтрами
]
```

**Стили TabBar:**
- **Активная вкладка:** Цвет #2679DB, fontWeight 600, fontSize 14
- **Неактивная:** Цвет #6B7280, fontWeight 500, fontSize 14
- **Индикатор:** Цвет #2679DB, толщина 2px

### 🎨 **Карточка поездки (_buildTripCard):**

**Структура карточки:**
```dart
Container(
  margin: EdgeInsets.only(bottom: 12),
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(color: #E5E7EB, width: 1),
    boxShadow: [...]
  ),
  child: InkWell(
    onTap: () => _showTripDetails(trip), // ← КЛИК ОТКРЫВАЕТ ДЕТАЛИ
    child: Stack([
      // ОСНОВНАЯ ИНФОРМАЦИЯ
      Column([
        // Номер грузовика (fontSize: 18, fontWeight: 700, color: #111827)
        Text(vehicle['number']),
        
        // Модель + Водитель (fontSize: 13, fontWeight: 500, color: #6B7280)
        Text('${vehicle['model']} • ${driver['name'].split(' ')[0]}'),
        
        // Маршрут (fontSize: 14, fontWeight: 600, color: #374151)
        Text('${start_location} → ${end_location}'),
        
        // Пункт пропуска (fontSize: 12, color: #9CA3AF)
        Text(border_crossing),
      ]),
      
      // СТАТУС (Positioned top: 0, right: 0)
      Container(
        padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
        decoration: BoxDecoration(
          color: statusBgColor,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: statusColor.withOpacity(0.2)),
        ),
        child: Row([
          // Круглая точка статуса (width: 6, height: 6)
          Container(decoration: BoxDecoration(color: statusColor, shape: circle)),
          Text(statusText), // fontSize: 11, fontWeight: 600
        ]),
      ),
      
      // ДАТА (Positioned bottom: 0, right: 0)
      Text(DateFormat('dd.MM.yyyy').format(start_date)),
    ])
  )
)
```

**Цвета статусов:**
- **ACTIVE:** statusColor: #059669, statusBgColor: #ECFDF5, text: "В пути"
- **COMPLETED:** statusColor: #6B7280, statusBgColor: #F9FAFB, text: "Завершен"  
- **PLANNED:** statusColor: #2563EB, statusBgColor: #EFF6FF, text: "Запланирован"

### 🔧 **Фильтры (График вкладка):**
- **Дата с/по:** DatePicker с локалью 'ru'
- **Водитель:** Modal bottom sheet с выбором
- **Транспорт:** Modal bottom sheet с выбором
- **Кнопка "Очистить фильтры"**

## 🎯 ДЕТАЛЬНАЯ СТРАНИЦА (TripDetailsScreen)

### 📱 **Общая структура:**
- **AppHeader** с кнопкой "Назад"
- **Прокручиваемый контент** (SingleChildScrollView)
- **4 основных блока:** Информация, Карта, Контакты, Дополнительно

### 📋 **Блок 1: Основная информация**
```dart
Container(
  margin: EdgeInsets.all(16),
  padding: EdgeInsets.all(20),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(16),
    border: Border.all(color: #E5E7EB),
    boxShadow: [...]
  ),
  child: Column([
    // ЗАГОЛОВОК С СТАТУСОМ
    Row([
      // Номер + модель (fontSize: 20, fontWeight: 700)
      Text('${vehicle['number']} • ${vehicle['model']}'),
      // Водитель (fontSize: 14, fontWeight: 500, color: #6B7280)
      Text('Водитель: ${driver['name']}'),
      
      // СТАТУС БЕЙДЖ (справа)
      Container(
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: statusColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: statusColor.withOpacity(0.2)),
        ),
        child: Row([
          Container(width: 8, height: 8, decoration: circle), // точка
          Text(statusText), // fontSize: 13, fontWeight: 600
        ]),
      ),
    ]),
    
    // ИНФОРМАЦИОННАЯ ПАНЕЛЬ
    Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: #F8FAFC,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: #E5E7EB),
      ),
      child: Column([
        _buildInfoRow('Маршрут', '${start_location} → ${end_location}'),
        _buildInfoRow('Время отправления', DateFormat('dd.MM.yyyy в HH:mm')),
        _buildInfoRow('Груз', cargo_type),
        _buildInfoSubtext('Объем: ${cargo_volume} м³ • Вес: ${cargo_weight} кг'),
        _buildInfoRow('Номер прицепа', trailer_number),
        _buildInfoRow('Пункт пропуска', border_crossing),
      ]),
    ),
    
    // ПРОГРЕСС (только для ACTIVE)
    if (status == 'ACTIVE') Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: #2679DB.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: #2679DB.withOpacity(0.1)),
      ),
      child: Column([
        Row([
          Text('Прогресс поездки'),
          Text('${(progress * 100).round()}%'), // fontSize: 16, fontWeight: 700
        ]),
        // Прогресс бар
        Container(
          height: 6,
          decoration: BoxDecoration(color: #E5E7EB, borderRadius: 3),
          child: FractionallySizedBox(
            widthFactor: progress,
            child: Container(decoration: BoxDecoration(color: #2679DB, borderRadius: 3)),
          ),
        ),
      ]),
    ),
  ])
)
```

### 🗺️ **Блок 2: Карта с маршрутом**
```dart
Container(
  height: 300,
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(16),
    boxShadow: [...]
  ),
  child: FlutterMap(
    options: MapOptions(
      initialCenter: routePoints.first,
      initialZoom: 6.0,
    ),
    children: [
      // ТАЙЛЫ КАРТЫ
      TileLayer(
        urlTemplate: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        subdomains: ['a', 'b', 'c', 'd'],
      ),
      
      // МАРШРУТ
      PolylineLayer(
        polylines: [Polyline(
          points: realRoutePoints,
          color: #2563EB,
          strokeWidth: 6.0,
          borderColor: Colors.white,
          borderStrokeWidth: 1.0,
        )],
      ),
      
      // МАРКЕРЫ
      MarkerLayer(markers: [
        // Начальная точка - синий круг
        Marker(
          point: routePoints.first,
          width: 20, height: 20,
          child: Container(
            decoration: BoxDecoration(
              color: #2563EB,
              shape: circle,
              border: Border.all(color: white, width: 2),
              boxShadow: [...]
            ),
            child: Container(width: 8, height: 8, decoration: white circle),
          ),
        ),
        
        // Конечная точка - зеленый круг  
        Marker(
          point: routePoints.last,
          width: 20, height: 20,
          child: Container(
            decoration: BoxDecoration(
              color: #34D399,
              shape: circle,
              border: Border.all(color: white, width: 2),
            ),
            child: Container(width: 8, height: 8, decoration: white circle),
          ),
        ),
        
        // Текущая позиция (только для ACTIVE)
        if (currentPosition != null) Marker(
          point: currentPosition,
          width: 50, height: 50,
          child: Container(
            decoration: BoxDecoration(
              color: #2679DB,
              borderRadius: 25,
              border: Border.all(color: white, width: 4),
              boxShadow: [...]
            ),
            child: Icon(Icons.local_shipping, color: white, size: 24),
          ),
        ),
      ]),
    ],
    
    // КНОПКИ УПРАВЛЕНИЯ
    Stack([
      // Полноэкранный режим (top: 12, right: 12)
      Positioned(child: IconButton(Icons.fullscreen)),
      
      // Центрирование карты (top: 12, left: 12)  
      Positioned(child: IconButton(Icons.center_focus_strong)),
    ]),
  ),
)
```

### 📞 **Блок 3: Контакты**
```dart
Container(
  padding: EdgeInsets.all(20),
  decoration: BoxDecoration(white background, rounded corners, shadow),
  child: Column([
    Text('Контакты'), // fontSize: 18, fontWeight: 700
    
    // Водитель
    Row([
      Container(
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: #2679DB.withOpacity(0.1),
          borderRadius: 12,
        ),
        child: Icon(Icons.person, color: #2679DB),
      ),
      Column([
        Text(driver['name']), // fontSize: 16, fontWeight: 600
        Text(driver['phone']), // fontSize: 14, color: #6B7280
      ]),
      // Кнопка звонка
      IconButton(Icons.phone, color: #10B981),
    ]),
  ]),
)
```

### ⚙️ **Вспомогательные методы:**

**_buildInfoRow():**
```dart
Widget _buildInfoRow(String label, String value) {
  return Row([
    Text(label), // fontSize: 14, fontWeight: 500, color: #6B7280
    Spacer(),
    Text(value), // fontSize: 14, fontWeight: 600, color: #1F2937
  ]);
}
```

**Расчет текущей позиции:**
```dart
LatLng _getCurrentPosition() {
  final progress = trip['progress'] as double;
  final start = routePoints.first;
  final end = routePoints.last;
  
  // Интерполяция позиции
  final lat = start.latitude + (end.latitude - start.latitude) * progress;
  final lng = start.longitude + (end.longitude - start.longitude) * progress;
  
  return LatLng(lat, lng);
}
```

## 🎯 КЛЮЧЕВЫЕ ОСОБЕННОСТИ:

### 🔄 **Навигация:**
- Клик на карточку → `Navigator.push(TripDetailsScreen)`
- Кнопка "Назад" в AppHeader
- Полноэкранная карта в модальном окне

### 📊 **Данные поездки:**
```dart
{
  'id': 1,
  'vehicle': {'number': '290 ATL 01', 'model': 'DAF XF 106'},
  'driver': {'name': 'Юнус Алиев', 'phone': '+7 (777) 159 03 06'},
  'status': 'ACTIVE', // ACTIVE, COMPLETED, PLANNED
  'start_location': 'Алматы',
  'end_location': 'Астана', 
  'cargo_type': 'Продукты питания',
  'cargo_volume': 15.5, // м³
  'cargo_weight': 12000, // кг
  'trailer_number': 'П 125 ATL 01',
  'border_crossing': 'Нур Жолы',
  'start_date': '2025-01-07T08:00:00',
  'estimated_arrival': '2025-01-07T20:00:00',
  'progress': 0.6, // 0.0 - 1.0
}
```

### 🎨 **Цветовая схема:**
- **Основной синий:** #2679DB
- **Зеленый (успех):** #10B981, #059669, #34D399
- **Серый (завершено):** #6B7280  
- **Фон:** #F8FAFC
- **Карточки:** #FFFFFF
- **Границы:** #E5E7EB
- **Текст главный:** #111827, #1F2937
- **Текст вторичный:** #6B7280, #9CA3AF

### 📐 **Размеры и отступы:**
- **Карточки:** margin 16px, padding 16-20px, borderRadius 12-16px
- **Тексты:** fontSize 11-20px, fontWeight 500-700
- **Иконки:** size 20-24px
- **Тени:** blurRadius 10-32px, offset (0, 2-16)

**ВСЯ ЭТА ИНФОРМАЦИЯ ДОЛЖНА БЫТЬ ТОЧНО ВОСПРОИЗВЕДЕНА В ВЕБ ВЕРСИИ!** 🎯 
 

## 🎯 СТРУКТУРА ЭКРАНА ЗАЕЗДОВ (TripsScreen)

### 📱 **Общая структура:**
- **3 вкладки:** "Активные", "Все заезды", "График"
- **TabController** для переключения вкладок
- **Фильтры** на третьей вкладке (дата, водитель, транспорт)

### 📋 **Вкладки (TabBar):**
```dart
tabs: [
  Tab(text: 'Активные'),     // Только ACTIVE статусы
  Tab(text: 'Все заезды'),   // Все поездки
  Tab(text: 'График'),       // С фильтрами
]
```

**Стили TabBar:**
- **Активная вкладка:** Цвет #2679DB, fontWeight 600, fontSize 14
- **Неактивная:** Цвет #6B7280, fontWeight 500, fontSize 14
- **Индикатор:** Цвет #2679DB, толщина 2px

### 🎨 **Карточка поездки (_buildTripCard):**

**Структура карточки:**
```dart
Container(
  margin: EdgeInsets.only(bottom: 12),
  padding: EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(color: #E5E7EB, width: 1),
    boxShadow: [...]
  ),
  child: InkWell(
    onTap: () => _showTripDetails(trip), // ← КЛИК ОТКРЫВАЕТ ДЕТАЛИ
    child: Stack([
      // ОСНОВНАЯ ИНФОРМАЦИЯ
      Column([
        // Номер грузовика (fontSize: 18, fontWeight: 700, color: #111827)
        Text(vehicle['number']),
        
        // Модель + Водитель (fontSize: 13, fontWeight: 500, color: #6B7280)
        Text('${vehicle['model']} • ${driver['name'].split(' ')[0]}'),
        
        // Маршрут (fontSize: 14, fontWeight: 600, color: #374151)
        Text('${start_location} → ${end_location}'),
        
        // Пункт пропуска (fontSize: 12, color: #9CA3AF)
        Text(border_crossing),
      ]),
      
      // СТАТУС (Positioned top: 0, right: 0)
      Container(
        padding: EdgeInsets.symmetric(horizontal: 10, vertical: 4),
        decoration: BoxDecoration(
          color: statusBgColor,
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: statusColor.withOpacity(0.2)),
        ),
        child: Row([
          // Круглая точка статуса (width: 6, height: 6)
          Container(decoration: BoxDecoration(color: statusColor, shape: circle)),
          Text(statusText), // fontSize: 11, fontWeight: 600
        ]),
      ),
      
      // ДАТА (Positioned bottom: 0, right: 0)
      Text(DateFormat('dd.MM.yyyy').format(start_date)),
    ])
  )
)
```

**Цвета статусов:**
- **ACTIVE:** statusColor: #059669, statusBgColor: #ECFDF5, text: "В пути"
- **COMPLETED:** statusColor: #6B7280, statusBgColor: #F9FAFB, text: "Завершен"  
- **PLANNED:** statusColor: #2563EB, statusBgColor: #EFF6FF, text: "Запланирован"

### 🔧 **Фильтры (График вкладка):**
- **Дата с/по:** DatePicker с локалью 'ru'
- **Водитель:** Modal bottom sheet с выбором
- **Транспорт:** Modal bottom sheet с выбором
- **Кнопка "Очистить фильтры"**

## 🎯 ДЕТАЛЬНАЯ СТРАНИЦА (TripDetailsScreen)

### 📱 **Общая структура:**
- **AppHeader** с кнопкой "Назад"
- **Прокручиваемый контент** (SingleChildScrollView)
- **4 основных блока:** Информация, Карта, Контакты, Дополнительно

### 📋 **Блок 1: Основная информация**
```dart
Container(
  margin: EdgeInsets.all(16),
  padding: EdgeInsets.all(20),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(16),
    border: Border.all(color: #E5E7EB),
    boxShadow: [...]
  ),
  child: Column([
    // ЗАГОЛОВОК С СТАТУСОМ
    Row([
      // Номер + модель (fontSize: 20, fontWeight: 700)
      Text('${vehicle['number']} • ${vehicle['model']}'),
      // Водитель (fontSize: 14, fontWeight: 500, color: #6B7280)
      Text('Водитель: ${driver['name']}'),
      
      // СТАТУС БЕЙДЖ (справа)
      Container(
        padding: EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: statusColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: statusColor.withOpacity(0.2)),
        ),
        child: Row([
          Container(width: 8, height: 8, decoration: circle), // точка
          Text(statusText), // fontSize: 13, fontWeight: 600
        ]),
      ),
    ]),
    
    // ИНФОРМАЦИОННАЯ ПАНЕЛЬ
    Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: #F8FAFC,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: #E5E7EB),
      ),
      child: Column([
        _buildInfoRow('Маршрут', '${start_location} → ${end_location}'),
        _buildInfoRow('Время отправления', DateFormat('dd.MM.yyyy в HH:mm')),
        _buildInfoRow('Груз', cargo_type),
        _buildInfoSubtext('Объем: ${cargo_volume} м³ • Вес: ${cargo_weight} кг'),
        _buildInfoRow('Номер прицепа', trailer_number),
        _buildInfoRow('Пункт пропуска', border_crossing),
      ]),
    ),
    
    // ПРОГРЕСС (только для ACTIVE)
    if (status == 'ACTIVE') Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: #2679DB.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: #2679DB.withOpacity(0.1)),
      ),
      child: Column([
        Row([
          Text('Прогресс поездки'),
          Text('${(progress * 100).round()}%'), // fontSize: 16, fontWeight: 700
        ]),
        // Прогресс бар
        Container(
          height: 6,
          decoration: BoxDecoration(color: #E5E7EB, borderRadius: 3),
          child: FractionallySizedBox(
            widthFactor: progress,
            child: Container(decoration: BoxDecoration(color: #2679DB, borderRadius: 3)),
          ),
        ),
      ]),
    ),
  ])
)
```

### 🗺️ **Блок 2: Карта с маршрутом**
```dart
Container(
  height: 300,
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(16),
    boxShadow: [...]
  ),
  child: FlutterMap(
    options: MapOptions(
      initialCenter: routePoints.first,
      initialZoom: 6.0,
    ),
    children: [
      // ТАЙЛЫ КАРТЫ
      TileLayer(
        urlTemplate: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
        subdomains: ['a', 'b', 'c', 'd'],
      ),
      
      // МАРШРУТ
      PolylineLayer(
        polylines: [Polyline(
          points: realRoutePoints,
          color: #2563EB,
          strokeWidth: 6.0,
          borderColor: Colors.white,
          borderStrokeWidth: 1.0,
        )],
      ),
      
      // МАРКЕРЫ
      MarkerLayer(markers: [
        // Начальная точка - синий круг
        Marker(
          point: routePoints.first,
          width: 20, height: 20,
          child: Container(
            decoration: BoxDecoration(
              color: #2563EB,
              shape: circle,
              border: Border.all(color: white, width: 2),
              boxShadow: [...]
            ),
            child: Container(width: 8, height: 8, decoration: white circle),
          ),
        ),
        
        // Конечная точка - зеленый круг  
        Marker(
          point: routePoints.last,
          width: 20, height: 20,
          child: Container(
            decoration: BoxDecoration(
              color: #34D399,
              shape: circle,
              border: Border.all(color: white, width: 2),
            ),
            child: Container(width: 8, height: 8, decoration: white circle),
          ),
        ),
        
        // Текущая позиция (только для ACTIVE)
        if (currentPosition != null) Marker(
          point: currentPosition,
          width: 50, height: 50,
          child: Container(
            decoration: BoxDecoration(
              color: #2679DB,
              borderRadius: 25,
              border: Border.all(color: white, width: 4),
              boxShadow: [...]
            ),
            child: Icon(Icons.local_shipping, color: white, size: 24),
          ),
        ),
      ]),
    ],
    
    // КНОПКИ УПРАВЛЕНИЯ
    Stack([
      // Полноэкранный режим (top: 12, right: 12)
      Positioned(child: IconButton(Icons.fullscreen)),
      
      // Центрирование карты (top: 12, left: 12)  
      Positioned(child: IconButton(Icons.center_focus_strong)),
    ]),
  ),
)
```

### 📞 **Блок 3: Контакты**
```dart
Container(
  padding: EdgeInsets.all(20),
  decoration: BoxDecoration(white background, rounded corners, shadow),
  child: Column([
    Text('Контакты'), // fontSize: 18, fontWeight: 700
    
    // Водитель
    Row([
      Container(
        padding: EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: #2679DB.withOpacity(0.1),
          borderRadius: 12,
        ),
        child: Icon(Icons.person, color: #2679DB),
      ),
      Column([
        Text(driver['name']), // fontSize: 16, fontWeight: 600
        Text(driver['phone']), // fontSize: 14, color: #6B7280
      ]),
      // Кнопка звонка
      IconButton(Icons.phone, color: #10B981),
    ]),
  ]),
)
```

### ⚙️ **Вспомогательные методы:**

**_buildInfoRow():**
```dart
Widget _buildInfoRow(String label, String value) {
  return Row([
    Text(label), // fontSize: 14, fontWeight: 500, color: #6B7280
    Spacer(),
    Text(value), // fontSize: 14, fontWeight: 600, color: #1F2937
  ]);
}
```

**Расчет текущей позиции:**
```dart
LatLng _getCurrentPosition() {
  final progress = trip['progress'] as double;
  final start = routePoints.first;
  final end = routePoints.last;
  
  // Интерполяция позиции
  final lat = start.latitude + (end.latitude - start.latitude) * progress;
  final lng = start.longitude + (end.longitude - start.longitude) * progress;
  
  return LatLng(lat, lng);
}
```

## 🎯 КЛЮЧЕВЫЕ ОСОБЕННОСТИ:

### 🔄 **Навигация:**
- Клик на карточку → `Navigator.push(TripDetailsScreen)`
- Кнопка "Назад" в AppHeader
- Полноэкранная карта в модальном окне

### 📊 **Данные поездки:**
```dart
{
  'id': 1,
  'vehicle': {'number': '290 ATL 01', 'model': 'DAF XF 106'},
  'driver': {'name': 'Юнус Алиев', 'phone': '+7 (777) 159 03 06'},
  'status': 'ACTIVE', // ACTIVE, COMPLETED, PLANNED
  'start_location': 'Алматы',
  'end_location': 'Астана', 
  'cargo_type': 'Продукты питания',
  'cargo_volume': 15.5, // м³
  'cargo_weight': 12000, // кг
  'trailer_number': 'П 125 ATL 01',
  'border_crossing': 'Нур Жолы',
  'start_date': '2025-01-07T08:00:00',
  'estimated_arrival': '2025-01-07T20:00:00',
  'progress': 0.6, // 0.0 - 1.0
}
```

### 🎨 **Цветовая схема:**
- **Основной синий:** #2679DB
- **Зеленый (успех):** #10B981, #059669, #34D399
- **Серый (завершено):** #6B7280  
- **Фон:** #F8FAFC
- **Карточки:** #FFFFFF
- **Границы:** #E5E7EB
- **Текст главный:** #111827, #1F2937
- **Текст вторичный:** #6B7280, #9CA3AF

### 📐 **Размеры и отступы:**
- **Карточки:** margin 16px, padding 16-20px, borderRadius 12-16px
- **Тексты:** fontSize 11-20px, fontWeight 500-700
- **Иконки:** size 20-24px
- **Тени:** blurRadius 10-32px, offset (0, 2-16)

**ВСЯ ЭТА ИНФОРМАЦИЯ ДОЛЖНА БЫТЬ ТОЧНО ВОСПРОИЗВЕДЕНА В ВЕБ ВЕРСИИ!** 🎯 
 
 
 
 