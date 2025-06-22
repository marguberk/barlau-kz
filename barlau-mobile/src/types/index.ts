// Типы данных для мобильного приложения BARLAU.KZ

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  role: 'SUPERADMIN' | 'ADMIN' | 'DIRECTOR' | 'DISPATCHER' | 'DRIVER' | 'ACCOUNTANT' | 'SUPPLIER' | 'TECH' | 'MANAGER';
  photo?: string;
  position?: string;
  is_active: boolean;
  is_archived: boolean;
  date_joined: string;
  current_latitude?: number;
  current_longitude?: number;
  last_location_update?: string;
  location_tracking_enabled?: boolean;
  experience?: string;
  education?: string;
  skills?: string;
  certifications?: string;
  languages?: string;
  desired_salary?: number;
  age?: number;
  location?: string;
  skype?: string;
  linkedin?: string;
  portfolio_url?: string;
  about_me?: string;
  key_skills?: string;
  achievements?: string;
  courses?: string;
  publications?: string;
  recommendations?: string;
  hobbies?: string;
  recommendation_file?: string;
  is_phone_verified?: boolean;
  firebase_uid?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Vehicle {
  id: number;
  number: string;
  brand: string;
  model: string;
  year: number;
  color?: string;
  description?: string;
  vehicle_type: 'CAR' | 'TRUCK' | 'SPECIAL';
  vehicle_type_display: string;
  status: 'ACTIVE' | 'INACTIVE' | 'MAINTENANCE';
  status_display: string;
  status_color: string;
  is_archived: boolean;
  driver?: {
    id: number;
    name: string;
    phone: string;
    photo?: string;
  };
  photo?: string;
  fuel_type?: 'DIESEL' | 'PETROL' | 'GAS' | 'HYBRID' | 'ELECTRIC';
  fuel_type_display?: string;
  fuel_consumption?: number;
  max_weight?: number;
  cargo_capacity?: number;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH';
  status: 'NEW' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED';
  assigned_to?: User;
  vehicle?: Vehicle;
  due_date: string;
  created_at: string;
  updated_at: string;
  created_by?: User;
}

export interface Notification {
  id: string;
  type: 'TASK' | 'WAYBILL' | 'EXPENSE' | 'SYSTEM' | 'DOCUMENT';
  title: string;
  message: string;
  link?: string;
  read: boolean;
  created_at: string;
}

export interface Waybill {
  id: number;
  number: string;
  date: string;
  vehicle: Vehicle;
  driver: User;
  departure_point: string;
  destination_point: string;
  cargo_description: string;
  cargo_weight: number;
  created_at: string;
  updated_at: string;
  created_by?: User;
}

export interface Trip {
  id: number;
  vehicle: Vehicle;
  driver: User;
  start_latitude: number;
  start_longitude: number;
  end_latitude: number;
  end_longitude: number;
  start_address?: string;
  end_address?: string;
  cargo_description?: string;
  date: string;
  created_at: string;
}

export interface DriverLocation {
  id: number;
  driver: User;
  latitude: number;
  longitude: number;
  timestamp: string;
  trip?: Trip;
}

export interface Expense {
  id: number;
  amount: number;
  category: 'FUEL' | 'MAINTENANCE' | 'REPAIR' | 'OTHER';
  description: string;
  date: string;
  receipt?: string;
  vehicle: Vehicle;
  created_by: User;
  status: 'PENDING' | 'APPROVED' | 'REJECTED';
  created_at: string;
}

// API Response Types
export interface ApiResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

// Navigation Types
export type RootStackParamList = {
  Login: undefined;
  Dashboard: undefined;
  Tasks: undefined;
  TaskDetail: { taskId: number };
  Vehicles: undefined;
  VehicleDetail: { vehicleId: number };
  Map: undefined;
  Profile: undefined;
  Notifications: undefined;
  Waybills: undefined;
  WaybillDetail: { waybillId: number };
  Trips: undefined;
  TripDetail: { tripId: number };
  Expenses: undefined;
  ExpenseDetail: { expenseId: number };
};

export type BottomTabParamList = {
  Dashboard: undefined;
  Tasks: undefined;
  Map: undefined;
  Vehicles: undefined;
  Profile: undefined;
}; 