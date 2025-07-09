import axios, { AxiosInstance, AxiosResponse } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Constants from 'expo-constants';
import { 
  ApiResponse, 
  LoginRequest, 
  LoginResponse, 
  User, 
  Trip, 
  Vehicle, 
  Employee, 
  Task 
} from '../types';

// Конфигурация API
const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8001' // Для разработки
  : 'https://barlau.kz'; // Для продакшена

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Добавляем токен к каждому запросу
    this.api.interceptors.request.use(async (config) => {
      const token = await AsyncStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Обработка ответов
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Токен истек, выходим из системы
          await AsyncStorage.removeItem('authToken');
          await AsyncStorage.removeItem('user');
        }
        return Promise.reject(error);
      }
    );
  }

  // Авторизация
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    try {
      const response: AxiosResponse<ApiResponse<LoginResponse>> = await this.api.post(
        '/api/auth/login/',
        credentials
      );
      
      if (response.data.success) {
        const { token, user } = response.data.data;
        await AsyncStorage.setItem('authToken', token);
        await AsyncStorage.setItem('user', JSON.stringify(user));
        return { token, user };
      }
      
      throw new Error(response.data.message || 'Ошибка входа');
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  // Выход из системы
  async logout(): Promise<void> {
    try {
      await this.api.post('/api/auth/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      await AsyncStorage.removeItem('authToken');
      await AsyncStorage.removeItem('user');
    }
  }

  // Получение текущего пользователя
  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<ApiResponse<User>> = await this.api.get('/api/auth/me/');
    return response.data.data;
  }

  // Поездки
  async getTrips(): Promise<Trip[]> {
    const response: AxiosResponse<ApiResponse<Trip[]>> = await this.api.get('/dashboard/api/trips/');
    return response.data.data || response.data; // Поддержка разных форматов ответа
  }

  async getTripById(id: number): Promise<Trip> {
    const response: AxiosResponse<ApiResponse<Trip>> = await this.api.get(`/dashboard/api/trips/${id}/`);
    return response.data.data;
  }

  // Транспорт
  async getVehicles(): Promise<Vehicle[]> {
    const response: AxiosResponse<ApiResponse<Vehicle[]>> = await this.api.get('/api/vehicles/');
    return response.data.data || response.data;
  }

  async getVehicleById(id: number): Promise<Vehicle> {
    const response: AxiosResponse<ApiResponse<Vehicle>> = await this.api.get(`/api/vehicles/${id}/`);
    return response.data.data;
  }

  // Сотрудники
  async getEmployees(): Promise<Employee[]> {
    const response: AxiosResponse<ApiResponse<Employee[]>> = await this.api.get('/api/employees/');
    return response.data.data || response.data;
  }

  async getEmployeeById(id: number): Promise<Employee> {
    const response: AxiosResponse<ApiResponse<Employee>> = await this.api.get(`/api/employees/${id}/`);
    return response.data.data;
  }

  // Задачи
  async getTasks(): Promise<Task[]> {
    const response: AxiosResponse<ApiResponse<Task[]>> = await this.api.get('/api/tasks/');
    return response.data.data || response.data;
  }

  async getTaskById(id: number): Promise<Task> {
    const response: AxiosResponse<ApiResponse<Task>> = await this.api.get(`/api/tasks/${id}/`);
    return response.data.data;
  }

  async updateTaskStatus(id: number, status: string): Promise<Task> {
    const response: AxiosResponse<ApiResponse<Task>> = await this.api.patch(`/api/tasks/${id}/`, { status });
    return response.data.data;
  }

  // Локации водителей
  async getDriverLocations(): Promise<any[]> {
    const response: AxiosResponse<any> = await this.api.get('/api/driver_locations/');
    return response.data;
  }

  // Уведомления
  async getNotifications(): Promise<any[]> {
    const response: AxiosResponse<any> = await this.api.get('/api/notifications/');
    return response.data;
  }

  async getUnreadNotificationsCount(): Promise<number> {
    const response: AxiosResponse<any> = await this.api.get('/api/notifications/unread_count/');
    return response.data.count || 0;
  }

  // Проверка подключения
  async checkConnection(): Promise<boolean> {
    try {
      await this.api.get('/api/health/');
      return true;
    } catch (error) {
      return false;
    }
  }
}

export default new ApiService(); 
 
 
 
 