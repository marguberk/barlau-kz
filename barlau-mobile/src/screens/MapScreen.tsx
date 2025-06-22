import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Animated,
  Dimensions,
  RefreshControl,
  PanResponder,
} from 'react-native';
import Svg, { Path, Circle, Rect, Defs, Pattern, G, Text as SvgText } from 'react-native-svg';
import { WebView } from 'react-native-webview';
import * as Location from 'expo-location';
import { useAuth } from '../context/AuthContext';
import { DriverLocation, Vehicle, Task } from '../types';
import { apiService } from '../services/api';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';

const { width, height } = Dimensions.get('window');

// Константы для карты
const MAP_WIDTH = width - 32;
const MAP_HEIGHT = 400;
const ALMATY_CENTER = { lat: 43.2380, lng: 76.9452 };

// Функция конвертации GPS координат в пиксели на карте
const coordsToPixels = (lat: number, lng: number, bounds: any, zoom: number = 1) => {
  const latRange = bounds.maxLat - bounds.minLat;
  const lngRange = bounds.maxLng - bounds.minLng;
  
  const x = ((lng - bounds.minLng) / lngRange) * MAP_WIDTH * zoom;
  const y = ((bounds.maxLat - lat) / latRange) * MAP_HEIGHT * zoom;
  
  return { x: Math.max(0, Math.min(MAP_WIDTH, x)), y: Math.max(0, Math.min(MAP_HEIGHT, y)) };
};

// Функция для получения границ карты на основе точек
const getBounds = (points: Array<{lat: number, lng: number}>) => {
  if (points.length === 0) {
    return {
      minLat: ALMATY_CENTER.lat - 0.1,
      maxLat: ALMATY_CENTER.lat + 0.1,
      minLng: ALMATY_CENTER.lng - 0.1,
      maxLng: ALMATY_CENTER.lng + 0.1,
    };
  }
  
  const lats = points.map(p => p.lat);
  const lngs = points.map(p => p.lng);
  
  const padding = 0.01; // Отступ
  return {
    minLat: Math.min(...lats) - padding,
    maxLat: Math.max(...lats) + padding,
    minLng: Math.min(...lngs) - padding,
    maxLng: Math.max(...lngs) + padding,
  };
};

const MapScreen: React.FC = () => {
  const { user } = useAuth();
  const [userLocation, setUserLocation] = useState<Location.LocationObject | null>(null);
  const [driverLocations, setDriverLocations] = useState<DriverLocation[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isTracking, setIsTracking] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'vehicles' | 'drivers' | 'tasks'>('all');
  const [selectedMarker, setSelectedMarker] = useState<any>(null);
  const [mapZoom, setMapZoom] = useState(1);
  const [mapOffset, setMapOffset] = useState({ x: 0, y: 0 });

  // Анимации
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(20)).current;

  useEffect(() => {
    requestLocationPermission();
    loadMapData();
    startAnimations();
    
    // Автоматическое обновление местоположения каждые 30 секунд
    const locationInterval = setInterval(() => {
      requestLocationPermission();
    }, 30000);

    return () => clearInterval(locationInterval);
  }, []);

  const startAnimations = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 600,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 500,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const requestLocationPermission = async () => {
    try {
      console.log('Запрашиваем разрешение на геолокацию...');
      
      const { status } = await Location.requestForegroundPermissionsAsync();
      
      if (status !== 'granted') {
        Alert.alert(
          'Разрешение на геолокацию',
          'Для работы карты необходимо разрешение на доступ к геолокации.',
          [{ text: 'OK' }]
        );
        return;
      }

      const location = await Location.getCurrentPositionAsync({
        accuracy: Location.Accuracy.High,
      });
      
      setUserLocation(location);
      
    } catch (error) {
      console.error('Ошибка получения геолокации:', error);
      Alert.alert(
        'Ошибка геолокации',
        'Не удалось получить ваше местоположение.',
        [{ text: 'OK' }]
      );
    }
  };

  const loadMapData = async () => {
    try {
      setIsLoading(true);
      
      // Загружаем данные параллельно
      const [locationsResult, vehiclesResult, tasksResult] = await Promise.allSettled([
        apiService.getDriverLocations(),
        apiService.getVehicles(),
        apiService.getTasks(),
      ]);

      if (locationsResult.status === 'fulfilled') {
        if (locationsResult.value && locationsResult.value.length > 0) {
          setDriverLocations(locationsResult.value);
        } else {
          // Если нет данных, оставляем пустой массив
          setDriverLocations([]);
        }
      }

      if (vehiclesResult.status === 'fulfilled' && vehiclesResult.value) {
        const vehiclesData = vehiclesResult.value.vehicles || vehiclesResult.value;
        setVehicles(Array.isArray(vehiclesData) ? vehiclesData : []);
      } else {
        // Если нет данных, оставляем пустой массив
        setVehicles([]);
      }

      if (tasksResult.status === 'fulfilled' && tasksResult.value) {
        setTasks(tasksResult.value.results || tasksResult.value);
      } else {
        // Тестовые данные для задач
        setTasks([
          {
            id: 1,
            title: 'Доставка груза в Астану',
            description: 'Перевозка строительных материалов',
            priority: 'HIGH',
            status: 'IN_PROGRESS',
            due_date: new Date(Date.now() + 86400000).toISOString(),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
          {
            id: 2,
            title: 'Загрузка на складе',
            description: 'Погрузка товаров для доставки',
            priority: 'MEDIUM',
            status: 'NEW',
            due_date: new Date(Date.now() + 172800000).toISOString(),
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          },
        ]);
      }

    } catch (error) {
      console.error('Ошибка загрузки данных:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadMapData();
    setRefreshing(false);
  };

  // Получаем все точки для отображения на карте
  const getAllMapPoints = () => {
    const points: Array<{lat: number, lng: number, type: string, data: any}> = [];
    
         // Добавляем водителей
     driverLocations.forEach(location => {
       if (location.latitude && location.longitude) {
         const lat = typeof location.latitude === 'string' ? parseFloat(location.latitude) : location.latitude;
         const lng = typeof location.longitude === 'string' ? parseFloat(location.longitude) : location.longitude;
         if (!isNaN(lat) && !isNaN(lng)) {
           points.push({
             lat,
             lng,
             type: 'driver',
             data: location
           });
         }
       }
     });

    // Добавляем пользователя
    if (userLocation) {
      points.push({
        lat: userLocation.coords.latitude,
        lng: userLocation.coords.longitude,
        type: 'user',
        data: userLocation
      });
    }

    return points;
  };

  // Создаем Pan Responder для интерактивности карты
  const panResponder = PanResponder.create({
    onMoveShouldSetPanResponder: () => true,
    onPanResponderMove: (evt, gestureState) => {
      setMapOffset({
        x: mapOffset.x + gestureState.dx,
        y: mapOffset.y + gestureState.dy
      });
    },
    onPanResponderRelease: () => {
      // Можно добавить инерцию или ограничения
    },
  });

  // Простая но эффективная карта с реальными координатами
  const renderSimpleRealMap = () => {
    const points = getAllMapPoints();
    
    // Реальные границы Алматы
    const ALMATY_BOUNDS = {
      minLat: 43.1500,
      maxLat: 43.3500,
      minLng: 76.7500,
      maxLng: 77.1500
    };
    
    // Функция конвертации GPS в пиксели
    const coordsToPixels = (lat: number, lng: number) => {
      const latRange = ALMATY_BOUNDS.maxLat - ALMATY_BOUNDS.minLat;
      const lngRange = ALMATY_BOUNDS.maxLng - ALMATY_BOUNDS.minLng;
      
      const x = ((lng - ALMATY_BOUNDS.minLng) / lngRange) * MAP_WIDTH;
      const y = ((ALMATY_BOUNDS.maxLat - lat) / latRange) * MAP_HEIGHT;
      
      return { 
        x: Math.max(20, Math.min(MAP_WIDTH - 20, x)), 
        y: Math.max(20, Math.min(MAP_HEIGHT - 20, y)) 
      };
    };

    return (
      <View style={styles.mapContainer}>
        {/* Карта-подложка */}
        <View style={styles.mapBackground}>
          <Svg width={MAP_WIDTH} height={MAP_HEIGHT} style={styles.map}>
            <Defs>
              {/* Градиент для карты */}
              <Pattern
                id="cityPattern"
                patternUnits="userSpaceOnUse"
                width="40"
                height="40"
              >
                <Rect width="40" height="40" fill="#e0f2fe" />
                <Path
                  d="M0 0L40 0L40 40L0 40Z M10 10L30 10L30 30L10 30Z"
                  fill="none"
                  stroke="#bfdbfe"
                  strokeWidth="0.5"
                />
                <Circle cx="20" cy="20" r="2" fill="#93c5fd" opacity="0.3" />
              </Pattern>
            </Defs>
            
            {/* Фон города */}
            <Rect
              width={MAP_WIDTH}
              height={MAP_HEIGHT}
              fill="url(#cityPattern)"
            />
            
            {/* Основные дороги Алматы (упрощенно) */}
            <Path
              d={`M 0 ${MAP_HEIGHT * 0.6} L ${MAP_WIDTH} ${MAP_HEIGHT * 0.6}`}
              stroke="#64748b"
              strokeWidth="3"
              opacity="0.4"
            />
            <Path
              d={`M ${MAP_WIDTH * 0.5} 0 L ${MAP_WIDTH * 0.5} ${MAP_HEIGHT}`}
              stroke="#64748b"
              strokeWidth="3"
              opacity="0.4"
            />
            <Path
              d={`M 0 ${MAP_HEIGHT * 0.3} L ${MAP_WIDTH} ${MAP_HEIGHT * 0.3}`}
              stroke="#64748b"
              strokeWidth="2"
              opacity="0.3"
            />
            <Path
              d={`M ${MAP_WIDTH * 0.3} 0 L ${MAP_WIDTH * 0.3} ${MAP_HEIGHT}`}
              stroke="#64748b"
              strokeWidth="2"
              opacity="0.3"
            />
            
            {/* Горы на заднем плане */}
            <Path
              d={`M 0 ${MAP_HEIGHT * 0.1} Q ${MAP_WIDTH * 0.2} ${MAP_HEIGHT * 0.05} ${MAP_WIDTH * 0.4} ${MAP_HEIGHT * 0.08} T ${MAP_WIDTH} ${MAP_HEIGHT * 0.12} L ${MAP_WIDTH} 0 L 0 0 Z`}
              fill="#94a3b8"
              opacity="0.2"
            />

            {/* Отображаем точки */}
            {points.map((point, index) => {
              const pixelCoords = coordsToPixels(point.lat, point.lng);
              
              if (point.type === 'driver') {
                return (
                  <G key={`driver-${point.data.id}-${index}`}>
                    {/* Анимированный пульс */}
                    <Circle
                      cx={pixelCoords.x}
                      cy={pixelCoords.y}
                      r="25"
                      fill="#10b981"
                      opacity="0.1"
                    />
                    <Circle
                      cx={pixelCoords.x}
                      cy={pixelCoords.y}
                      r="18"
                      fill="#10b981"
                      opacity="0.2"
                    />
                    <Circle
                      cx={pixelCoords.x}
                      cy={pixelCoords.y}
                      r="12"
                      fill="#10b981"
                      stroke="white"
                      strokeWidth="3"
                      onPress={() => {
                        const driver = point.data.driver;
                        Alert.alert(
                          `🚛 ${driver?.first_name} ${driver?.last_name}`,
                          `📞 ${driver?.phone || 'Нет телефона'}\n📍 ${point.lat.toFixed(6)}, ${point.lng.toFixed(6)}\n🕐 ${new Date(point.data.timestamp).toLocaleTimeString('ru-RU')}`,
                          [{ text: 'OK' }]
                        );
                      }}
                    />
                    {/* Иконка водителя */}
                    <SvgText
                      x={pixelCoords.x}
                      y={pixelCoords.y + 4}
                      fontSize="14"
                      fill="white"
                      textAnchor="middle"
                      fontWeight="bold"
                    >
                      🚛
                    </SvgText>
                  </G>
                );
              } else if (point.type === 'user') {
                return (
                  <G key={`user-${index}`}>
                    {/* Пульсирующий круг для пользователя */}
                    <Circle
                      cx={pixelCoords.x}
                      cy={pixelCoords.y}
                      r="20"
                      fill="#2563eb"
                      opacity="0.1"
                    />
                    <Circle
                      cx={pixelCoords.x}
                      cy={pixelCoords.y}
                      r="10"
                      fill="#2563eb"
                      stroke="white"
                      strokeWidth="3"
                      onPress={() => {
                        Alert.alert(
                          '📍 Ваше местоположение',
                          `📍 ${point.lat.toFixed(6)}, ${point.lng.toFixed(6)}\n🕐 ${userLocation ? new Date(userLocation.timestamp).toLocaleTimeString('ru-RU') : ''}`,
                          [{ text: 'OK' }]
                        );
                      }}
                    />
                    {/* Иконка местоположения */}
                    <SvgText
                      x={pixelCoords.x}
                      y={pixelCoords.y + 3}
                      fontSize="10"
                      fill="white"
                      textAnchor="middle"
                      fontWeight="bold"
                    >
                      📍
                    </SvgText>
                  </G>
                );
              }
              return null;
            })}
          </Svg>
        </View>

        {/* Информационная панель */}
        <View style={styles.mapInfo}>
          <View style={styles.mapInfoContent}>
            <Text style={styles.mapTitle}>🗺️ BARLAU Карта Алматы</Text>
            <Text style={styles.mapSubtitle}>Отслеживание {points.length} объектов в реальном времени</Text>
            <View style={styles.mapLegend}>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: '#10b981' }]} />
                <Text style={styles.legendText}>Водители: {driverLocations.length}</Text>
              </View>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: '#2563eb' }]} />
                <Text style={styles.legendText}>Ваше местоположение: {userLocation ? '1' : '0'}</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Координаты в углу */}
        <View style={styles.coordinatesDisplay}>
          <Text style={styles.coordinatesText}>
            🌐 Алматы: {ALMATY_CENTER.lat.toFixed(4)}, {ALMATY_CENTER.lng.toFixed(4)}
          </Text>
        </View>

        {/* Кнопка обновления */}
        <TouchableOpacity
          style={styles.refreshButton}
          onPress={() => {
            loadMapData();
            requestLocationPermission();
          }}
        >
          <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
            <Path
              d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <Path
              d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </Svg>
        </TouchableOpacity>
      </View>
    );
  };

  const toggleTracking = async () => {
    if (isTracking) {
      setIsTracking(false);
      Alert.alert('Отслеживание остановлено', 'Автоматическое обновление местоположения отключено.');
    } else {
      await requestLocationPermission();
      setIsTracking(true);
      Alert.alert('Отслеживание включено', 'Ваше местоположение будет обновляться автоматически.');
    }
  };

  const FilterButton = ({ 
    type, 
    label, 
    icon, 
    count 
  }: {
    type: typeof selectedFilter;
    label: string;
    icon: React.ReactNode;
    count: number;
  }) => (
    <TouchableOpacity
      style={[
        styles.filterButton,
        selectedFilter === type && styles.filterButtonActive
      ]}
      onPress={() => setSelectedFilter(type)}
    >
      {icon}
      <Text style={[
        styles.filterButtonText,
        selectedFilter === type && styles.filterButtonTextActive
      ]}>
        {label}
      </Text>
                     <Badge 
                 variant={selectedFilter === type ? 'default' : 'secondary'}
               >
                 {count.toString()}
               </Badge>
    </TouchableOpacity>
  );

  const MapItem = ({ 
    title, 
    subtitle, 
    status, 
    icon, 
    onPress 
  }: {
    title: string;
    subtitle: string;
    status: string;
    icon: React.ReactNode;
    onPress?: () => void;
  }) => (
    <TouchableOpacity style={styles.mapItem} onPress={onPress}>
      <View style={styles.mapItemIcon}>
        {icon}
      </View>
      <View style={styles.mapItemContent}>
        <Text style={styles.mapItemTitle}>{title}</Text>
        <Text style={styles.mapItemSubtitle}>{subtitle}</Text>
      </View>
      <Badge variant="secondary">{status}</Badge>
    </TouchableOpacity>
  );

  const getFilteredData = (): Array<{id: string; title: string; subtitle: string; status: string; icon: React.ReactNode}> => {
    let data: Array<{id: string; title: string; subtitle: string; status: string; icon: React.ReactNode}> = [];

    if (selectedFilter === 'all' || selectedFilter === 'vehicles') {
      vehicles.forEach((vehicle, index) => {
                 data.push({
           id: `vehicle-${vehicle.id}-${index}`,
           title: vehicle.number,
           subtitle: `${vehicle.brand} ${vehicle.model}`,
           status: vehicle.status === 'ACTIVE' ? 'Активен' : 'Неактивен',
          icon: (
            <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
              <Path d="M3 17h2l.5-2h13l.5 2h2v-5l-2-7H5l-2 7v5z" fill="#2563eb" />
              <Circle cx="7.5" cy="17.5" r="1.5" fill="#374151" />
              <Circle cx="16.5" cy="17.5" r="1.5" fill="#374151" />
            </Svg>
          ),
        });
      });
    }

    if (selectedFilter === 'all' || selectedFilter === 'drivers') {
      driverLocations.forEach((location, index) => {
        const driver = location.driver;
        data.push({
          id: `driver-${location.id}-${index}`,
          title: driver ? `${driver.first_name} ${driver.last_name}` : 'Неизвестный водитель',
          subtitle: driver?.phone || 'Нет телефона',
          status: 'Активен',
          icon: (
            <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
              <Circle cx="12" cy="12" r="10" fill="#10b981" />
              <Path d="M12 6v6l4 2" stroke="white" strokeWidth="2" strokeLinecap="round" />
            </Svg>
          ),
        });
      });
    }

    if (selectedFilter === 'all' || selectedFilter === 'tasks') {
      tasks.forEach((task, index) => {
        data.push({
          id: `task-${task.id}-${index}`,
          title: task.title,
          subtitle: task.description,
          status: task.status,
          icon: (
            <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
              <Rect x="3" y="3" width="18" height="18" rx="2" fill="#f59e0b" />
              <Path d="M9 12l2 2 4-4" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </Svg>
          ),
        });
      });
    }

    return data;
  };

  const filteredData = getFilteredData();

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View 
        style={[
          styles.content,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }]
          }
        ]}
      >
        {/* Заголовок */}
        <View style={styles.header}>
          <View style={styles.headerContent}>
            <Text style={styles.title}>Карта</Text>
            <TouchableOpacity
              style={styles.locationButton}
              onPress={requestLocationPermission}
            >
              <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
                <Circle cx="12" cy="12" r="10" stroke="#2563eb" strokeWidth="2" />
                <Circle cx="12" cy="12" r="3" fill="#2563eb" />
              </Svg>
            </TouchableOpacity>
          </View>
          <Text style={styles.subtitle}>
            Отслеживание транспорта и персонала{'\n'}в реальном времени
          </Text>
        </View>

        <ScrollView 
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
        >
          {/* Реальная интерактивная карта */}
          {renderSimpleRealMap()}

          {/* Фильтры */}
          <View style={styles.filtersContainer}>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <View style={styles.filters}>
                <FilterButton
                  type="all"
                  label="Все"
                  count={driverLocations.length + vehicles.length + tasks.length}
                  icon={
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Circle cx="12" cy="12" r="10" stroke={selectedFilter === 'all' ? '#ffffff' : '#2563eb'} strokeWidth="2" />
                      <Path d="M12 6v6l4 2" stroke={selectedFilter === 'all' ? '#ffffff' : '#2563eb'} strokeWidth="2" strokeLinecap="round" />
                    </Svg>
                  }
                />
                <FilterButton
                  type="vehicles"
                  label="Транспорт"
                  count={vehicles.length}
                  icon={
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path d="M3 17h2l.5-2h13l.5 2h2v-5l-2-7H5l-2 7v5z" fill={selectedFilter === 'vehicles' ? '#ffffff' : '#2563eb'} />
                      <Circle cx="7.5" cy="17.5" r="1.5" fill={selectedFilter === 'vehicles' ? '#ffffff' : '#374151'} />
                      <Circle cx="16.5" cy="17.5" r="1.5" fill={selectedFilter === 'vehicles' ? '#ffffff' : '#374151'} />
                    </Svg>
                  }
                />
                <FilterButton
                  type="drivers"
                  label="Водители"
                  count={driverLocations.length}
                  icon={
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Circle cx="12" cy="12" r="10" fill={selectedFilter === 'drivers' ? '#ffffff' : '#10b981'} />
                      <Path d="M12 6v6l4 2" stroke={selectedFilter === 'drivers' ? '#10b981' : 'white'} strokeWidth="2" strokeLinecap="round" />
                    </Svg>
                  }
                />
                <FilterButton
                  type="tasks"
                  label="Задачи"
                  count={tasks.length}
                  icon={
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Rect x="3" y="3" width="18" height="18" rx="2" fill={selectedFilter === 'tasks' ? '#ffffff' : '#f59e0b'} />
                      <Path d="M9 12l2 2 4-4" stroke={selectedFilter === 'tasks' ? '#f59e0b' : 'white'} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </Svg>
                  }
                />
              </View>
            </ScrollView>
          </View>

          {/* Список объектов на карте */}
          <Card style={styles.objectsCard}>
            <View style={styles.objectsHeader}>
              <Text style={styles.objectsTitle}>Объекты на карте</Text>
                             <Badge variant="default">{filteredData.length.toString()}</Badge>
            </View>
            
            {isLoading ? (
              <View style={styles.loadingContainer}>
                <Text style={styles.loadingText}>Загрузка данных...</Text>
              </View>
            ) : filteredData.length > 0 ? (
              <View style={styles.objectsList}>
                {filteredData.map((item) => (
                  <MapItem
                    key={item.id}
                    title={item.title}
                    subtitle={item.subtitle}
                    status={item.status}
                    icon={item.icon}
                    onPress={() => {
                      Alert.alert(
                        item.title,
                        `${item.subtitle}\nСтатус: ${item.status}`,
                        [{ text: 'OK' }]
                      );
                    }}
                  />
                ))}
              </View>
            ) : (
              <View style={styles.emptyContainer}>
                <Text style={styles.emptyText}>Нет данных для отображения</Text>
              </View>
            )}
          </Card>

          {/* Информация о местоположении */}
          {userLocation && (
            <Card style={styles.locationCard}>
              <View style={styles.locationHeader}>
                <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
                  <Circle cx="12" cy="12" r="10" stroke="#2563eb" strokeWidth="2" />
                  <Circle cx="12" cy="12" r="3" fill="#2563eb" />
                </Svg>
                <Text style={styles.locationTitle}>Ваше местоположение</Text>
              </View>
              <Text style={styles.locationCoords}>
                📍 {userLocation.coords.latitude.toFixed(6)}, {userLocation.coords.longitude.toFixed(6)}
              </Text>
              <Text style={styles.locationTime}>
                🕒 Обновлено: {new Date(userLocation.timestamp).toLocaleTimeString('ru-RU')}
              </Text>
            </Card>
          )}

          {/* Кнопки управления */}
          <View style={styles.controlsContainer}>
                         <Button
               onPress={toggleTracking}
               variant={isTracking ? "secondary" : "default"}
               style={styles.controlButton}
             >
               {isTracking ? "Остановить отслеживание" : "Определить местоположение"}
             </Button>
          </View>
        </ScrollView>
      </Animated.View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    flex: 1,
  },
  header: {
    paddingHorizontal: 16,
    paddingVertical: 20,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  locationButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#f1f5f9',
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    lineHeight: 24,
  },
  mapContainer: {
    margin: 16,
    borderRadius: 12,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
    overflow: 'hidden',
    position: 'relative',
  },
     map: {
     flex: 1,
     backgroundColor: '#f0f9ff',
   },
  mapInfo: {
    position: 'absolute',
    top: 16,
    left: 16,
    right: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 8,
    padding: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  mapInfoContent: {
    alignItems: 'center',
  },
  mapTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#1e293b',
    marginBottom: 4,
  },
  mapSubtitle: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 8,
  },
  mapLegend: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 4,
  },
  legendText: {
    fontSize: 12,
    color: '#64748b',
  },
  mapControls: {
    position: 'absolute',
    top: 100,
    right: 16,
    flexDirection: 'column',
  },
  mapControlButton: {
    width: 40,
    height: 40,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  mapControlText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#2563eb',
  },
  coordinatesDisplay: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    borderRadius: 6,
    paddingHorizontal: 8,
    paddingVertical: 4,
  },
  coordinatesText: {
    fontSize: 10,
    color: '#ffffff',
    fontFamily: 'monospace',
  },
  filtersContainer: {
    marginHorizontal: 16,
    marginBottom: 16,
  },
  filters: {
    flexDirection: 'row',
    paddingHorizontal: 4,
  },
  filterButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginHorizontal: 4,
    borderRadius: 24,
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#e2e8f0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  filterButtonActive: {
    backgroundColor: '#2563eb',
    borderColor: '#2563eb',
  },
  filterButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#64748b',
    marginLeft: 8,
    marginRight: 8,
  },
  filterButtonTextActive: {
    color: '#ffffff',
  },
  objectsCard: {
    margin: 16,
  },
  objectsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  objectsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1e293b',
  },
  objectsList: {
    gap: 12,
  },
  mapItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#f8fafc',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  mapItemIcon: {
    marginRight: 12,
  },
  mapItemContent: {
    flex: 1,
  },
  mapItemTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    marginBottom: 4,
  },
  mapItemSubtitle: {
    fontSize: 14,
    color: '#64748b',
  },
  loadingContainer: {
    padding: 32,
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#64748b',
  },
  emptyContainer: {
    padding: 32,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 16,
    color: '#64748b',
  },
  locationCard: {
    margin: 16,
  },
  locationHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  locationTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1e293b',
    marginLeft: 8,
  },
  locationCoords: {
    fontSize: 14,
    color: '#64748b',
    marginBottom: 4,
    fontFamily: 'monospace',
  },
  locationTime: {
    fontSize: 12,
    color: '#94a3b8',
  },
  controlsContainer: {
    margin: 16,
    marginBottom: 32,
  },
     controlButton: {
     marginBottom: 12,
   },
   mapBackground: {
     backgroundColor: '#f0f9ff',
   },
   refreshButton: {
     position: 'absolute',
     top: 100,
     left: 16,
     width: 40,
     height: 40,
     backgroundColor: '#2563eb',
     borderRadius: 20,
     justifyContent: 'center',
     alignItems: 'center',
     shadowColor: '#000',
     shadowOffset: { width: 0, height: 2 },
     shadowOpacity: 0.1,
     shadowRadius: 4,
     elevation: 2,
   },
});

export default MapScreen; 