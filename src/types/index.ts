// Типы для навигации
export type RootStackParamList = {
  Login: undefined;
  Dashboard: undefined;
};

export type BottomTabParamList = {
  Dashboard: undefined;
  Tasks: undefined;
  Map: undefined;
  Vehicles: undefined;
  Employees: undefined;
};

// Типы для данных
export interface User {
  id: number;
  username: string;
  email?: string;
  first_name: string;
  last_name: string;
  role: string;
}

export interface Trip {
  id: number;
  number: string;
  route: string;
  driver: string;
  vehicle: string;
  status: string;
  start_date: string;
  end_date?: string;
  coordinates?: {
    lat: number;
    lng: number;
  };
}

export interface Vehicle {
  id: number;
  brand: string;
  model: string;
  number: string;
  year: number;
  status: string;
  driver?: string;
}

export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  position: string;
  phone?: string;
  email?: string;
  photo?: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed';
  priority: 'low' | 'medium' | 'high';
  assigned_to: number;
  due_date?: string;
  created_at: string;
}

// API Response типы
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  token: string;
  user: User;
} 
 
 
 
 