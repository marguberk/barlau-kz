import axios, { AxiosInstance, AxiosResponse } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { 
  User, 
  Vehicle, 
  Task, 
  Notification, 
  Waybill, 
  Trip, 
  DriverLocation, 
  Expense,
  ApiResponse,
  AuthTokens,
  LoginCredentials
} from '../types';

// Настройка базового URL для API
// Определяем URL в зависимости от платформы
import { Platform } from 'react-native';

const getBaseURL = () => {
  // Временно используем локальный сервер, пока не развернем Django API на barlau.kz
  if (Platform.OS === 'android') {
    return 'http://192.168.27.223:8000'; // Android эмулятор - IP Mac
  } else if (Platform.OS === 'ios') {
    return 'http://192.168.27.223:8000'; // iOS симулятор - IP Mac
  } else {
    return 'http://192.168.27.223:8000'; // Веб и другие платформы - IP Mac
  }
};

const BASE_URL = getBaseURL();

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Настройка интерсептора для автоматического добавления токена
    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Настройка интерсептора для обработки ошибок авторизации
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Токен истек, пытаемся обновить
          const refreshToken = await AsyncStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const response = await this.refreshToken(refreshToken);
              await AsyncStorage.setItem('access_token', response.access);
              // Повторяем исходный запрос
              return this.api.request(error.config);
            } catch (refreshError) {
              // Не удалось обновить токен, выходим из системы
              await this.logout();
              throw refreshError;
            }
          }
        }
        return Promise.reject(error);
      }
    );
  }

  // Методы аутентификации
  async login(credentials: LoginCredentials): Promise<{ tokens: AuthTokens; user: User }> {
    try {
      console.log('Отправка запроса на вход:', `${BASE_URL}/api/v1/auth/token/`);
      const response = await this.api.post('/api/v1/auth/token/', credentials);
      const { access, refresh } = response.data;
      
      // Получаем информацию о пользователе
      const userResponse = await this.api.get('/api/v1/users/me/', {
        headers: { Authorization: `Bearer ${access}` }
      });
      const user = userResponse.data;
      
      await AsyncStorage.setItem('access_token', access);
      await AsyncStorage.setItem('refresh_token', refresh);
      await AsyncStorage.setItem('user', JSON.stringify(user));
      
      return { tokens: { access, refresh }, user };
    } catch (error: any) {
      console.error('Login error:', error);
      
      // Добавляем более подробную информацию об ошибке
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
      }
      
      throw error;
    }
  }

  async logout(): Promise<void> {
    await AsyncStorage.multiRemove(['access_token', 'refresh_token', 'user']);
  }

  async refreshToken(refreshToken: string): Promise<AuthTokens> {
    const response = await this.api.post('/api/v1/auth/token/refresh/', { refresh: refreshToken });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.api.get('/api/v1/users/me/');
    return response.data;
  }

  // Получить базовый URL
  getBaseURL(): string {
    return getBaseURL();
  }

  // Методы для работы с пользователями
  async getUsers(): Promise<ApiResponse<User>> {
    // Загружаем всех пользователей (увеличиваем лимит)
    const response = await this.api.get('/api/v1/users/?page_size=100');
    return response.data;
  }

  async getUser(id: number): Promise<User> {
    const response = await this.api.get(`/api/v1/users/${id}/`);
    return response.data;
  }

  // Методы для работы с задачами
  async getTasks(): Promise<ApiResponse<Task>> {
    const response = await this.api.get('/api/v1/tasks/');
    return response.data;
  }

  async getTask(id: number): Promise<Task> {
    const response = await this.api.get(`/api/v1/tasks/${id}/`);
    return response.data;
  }

  async updateTaskStatus(id: number, status: Task['status']): Promise<Task> {
    const response = await this.api.patch(`/api/v1/tasks/${id}/`, { status });
    return response.data;
  }

  // Методы для работы с транспортом
  async getVehicles(): Promise<{ vehicles: Vehicle[]; count: number }> {
    try {
      const response = await this.api.get('/api/vehicles/');
      console.log('API Response:', response.data);
      
      // Проверяем структуру ответа
      if (response.data.results) {
        // Преобразуем данные в нужный формат
        const vehicles: Vehicle[] = response.data.results.map((item: any) => ({
          id: item.id,
          number: item.number,
          brand: item.brand,
          model: item.model,
          year: item.year,
          color: item.color,
          description: item.description,
          vehicle_type: item.vehicle_type,
          vehicle_type_display: this.getVehicleTypeDisplay(item.vehicle_type),
          status: item.status,
          status_display: this.getStatusDisplay(item.status),
          status_color: this.getStatusColor(item.status),
          is_archived: item.is_archived || false,
          driver: item.driver_details ? {
            id: item.driver_details.id,
            name: `${item.driver_details.first_name} ${item.driver_details.last_name}`.trim(),
            phone: item.driver_details.phone,
            photo: item.driver_details.photo
          } : undefined,
          photo: item.main_photo_url ? `${BASE_URL}${item.main_photo_url}` : undefined,
          fuel_type: item.fuel_type,
          fuel_type_display: this.getFuelTypeDisplay(item.fuel_type),
          fuel_consumption: item.fuel_consumption ? parseFloat(item.fuel_consumption) : undefined,
          max_weight: item.max_weight ? parseFloat(item.max_weight) : undefined,
          cargo_capacity: item.cargo_capacity ? parseFloat(item.cargo_capacity) : undefined,
          created_at: item.created_at,
          updated_at: item.updated_at
        }));
        
        return { vehicles, count: response.data.count || vehicles.length };
      } else {
        console.warn('Unexpected API response structure:', response.data);
        return { vehicles: [], count: 0 };
      }
    } catch (error) {
      console.error('Error fetching vehicles:', error);
      throw error;
    }
  }

  // Вспомогательные методы для отображения
  private getVehicleTypeDisplay(type: string): string {
    switch (type) {
      case 'CAR': return 'Легковой';
      case 'TRUCK': return 'Грузовик';
      case 'SPECIAL': return 'Спецтехника';
      default: return type;
    }
  }

  private getStatusDisplay(status: string): string {
    switch (status) {
      case 'ACTIVE': return 'Активен';
      case 'INACTIVE': return 'Неактивен';
      case 'MAINTENANCE': return 'На ТО';
      default: return status;
    }
  }

  private getStatusColor(status: string): string {
    switch (status) {
      case 'ACTIVE': return '#10B981';
      case 'INACTIVE': return '#6B7280';
      case 'MAINTENANCE': return '#F59E0B';
      default: return '#6B7280';
    }
  }

  private getFuelTypeDisplay(type?: string): string {
    if (!type) return '';
    switch (type) {
      case 'DIESEL': return 'Дизель';
      case 'PETROL': return 'Бензин';
      case 'GAS': return 'Газ';
      case 'HYBRID': return 'Гибрид';
      case 'ELECTRIC': return 'Электро';
      default: return type;
    }
  }

  async getVehicle(id: number): Promise<Vehicle> {
    const response = await this.api.get(`/api/v1/vehicles/${id}/`);
    return response.data;
  }

  // Методы для работы с уведомлениями
  async getNotifications(): Promise<ApiResponse<Notification>> {
    const response = await this.api.get('/core/notifications/');
    return response.data;
  }

  async markNotificationAsRead(id: string): Promise<void> {
    await this.api.patch(`/core/notifications/${id}/`, { read: true });
  }

  // Методы для работы с путевыми листами
  async getWaybills(): Promise<ApiResponse<Waybill>> {
    const response = await this.api.get('/core/waybills/');
    return response.data;
  }

  async getWaybill(id: number): Promise<Waybill> {
    const response = await this.api.get(`/core/waybills/${id}/`);
    return response.data;
  }

  async createWaybill(data: Partial<Waybill>): Promise<Waybill> {
    const response = await this.api.post('/core/waybills/', data);
    return response.data;
  }

  // Методы для работы с поездками
  async getTrips(): Promise<ApiResponse<Trip>> {
    const response = await this.api.get('/core/trips/');
    return response.data;
  }

  async createTrip(data: Partial<Trip>): Promise<Trip> {
    const response = await this.api.post('/core/trips/', data);
    return response.data;
  }

  async deleteTrip(id: number): Promise<void> {
    await this.api.delete(`/core/trips/${id}/`);
  }

  // Методы для работы с геолокацией
  async getDriverLocations(): Promise<DriverLocation[]> {
    try {
      const response = await this.api.get('/api/driver_locations/');
      return response.data;
    } catch (error: any) {
      console.error('Driver locations error:', error);
      
      if (error.response) {
        console.error('Response status:', error.response.status);
        console.error('Response data:', error.response.data);
        
        // Если ошибка авторизации, пробуем обновить токен
        if (error.response.status === 401 || error.response.status === 403) {
          console.log('Ошибка авторизации, проверяем токен...');
          const token = await AsyncStorage.getItem('access_token');
          console.log('Текущий токен:', token ? 'есть' : 'отсутствует');
        }
      }
      
      throw error;
    }
  }

  async sendLocation(latitude: number, longitude: number): Promise<DriverLocation> {
    const response = await this.api.post('/api/driver_locations/', {
      latitude,
      longitude,
    });
    return response.data;
  }

  // Методы для работы с расходами
  async getExpenses(): Promise<ApiResponse<Expense>> {
    const response = await this.api.get('/logistics/expenses/');
    return response.data;
  }

  async createExpense(data: Partial<Expense>): Promise<Expense> {
    const response = await this.api.post('/logistics/expenses/', data);
    return response.data;
  }

  // Методы для работы с сотрудниками
  async downloadEmployeePDF(employeeId: number): Promise<any> {
    try {
      const response = await this.api.get(`/api/employees/${employeeId}/pdf/`, {
        responseType: 'blob',
      });
      return response.data;
    } catch (error: any) {
      console.error('PDF download error:', error);
      
      if (error.response) {
        console.error('PDF Response status:', error.response.status);
        console.error('PDF Response data:', error.response.data);
      }
      
      throw error;
    }
  }

  // Методы для работы с профилем
  async updateProfile(data: Partial<User>): Promise<User> {
    const response = await this.api.patch('/core/profile/', data);
    return response.data;
  }

  async uploadProfilePhoto(photo: string): Promise<User> {
    const formData = new FormData();
    formData.append('photo', {
      uri: photo,
      type: 'image/jpeg',
      name: 'profile.jpg',
    } as any);

    const response = await this.api.post('/core/profile/photo/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  // Методы для работы с картой
  async getMapData(): Promise<{ vehicles: Vehicle[]; tasks: Task[] }> {
    const response = await this.api.get('/map/');
    return response.data;
  }

  async updateTrackingStatus(enabled: boolean): Promise<void> {
    await this.api.post('/map/tracking_status/', { 
      location_tracking_enabled: enabled 
    });
  }
}

export const apiService = new ApiService();
export default apiService; 