import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ActivityIndicator } from 'react-native';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Провайдеры
import { AuthProvider, useAuth } from './src/context/AuthContext';

// Экраны
import LoginScreen from './src/screens/LoginScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import TasksScreen from './src/screens/TasksScreen';
import MapScreen from './src/screens/MapScreen';
import EmployeesScreen from './src/screens/EmployeesScreen';
import VehiclesScreen from './src/screens/VehiclesScreen';

// Компоненты
import SvgIcon from './src/components/SvgIcon';

// Типы навигации
import { RootStackParamList, BottomTabParamList } from './src/types';

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<BottomTabParamList>();

// Навигация для авторизованных пользователей
const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarStyle: styles.tabBar,
        tabBarActiveTintColor: '#2563EB',
        tabBarInactiveTintColor: '#64748B',
        tabBarLabelStyle: styles.tabLabel,
        headerShown: false,
      }}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{
          tabBarLabel: 'Главная',
          tabBarIcon: ({ color, focused }) => (
            <SvgIcon name="Dashboard" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Tasks"
        component={TasksScreen}
        options={{
          tabBarLabel: 'Задачи',
          tabBarIcon: ({ color, focused }) => (
            <SvgIcon name="Tasks" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Map"
        component={MapScreen}
        options={{
          tabBarLabel: 'Карта',
          tabBarIcon: ({ color, focused }) => (
            <SvgIcon name="Map" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Vehicles"
        component={VehiclesScreen}
        options={{
          tabBarLabel: 'Грузовики',
          tabBarIcon: ({ color, focused }) => (
            <SvgIcon name="Vehicles" focused={focused} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profile"
        component={EmployeesScreen}
        options={{
          tabBarLabel: 'Сотрудники',
          tabBarIcon: ({ color, focused }) => (
            <SvgIcon name="Employees" focused={focused} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

// Заглушки для экранов (создадим позже)
const TasksPlaceholder = () => (
  <View style={styles.placeholder}>
    <Text style={styles.placeholderText}>Экран задач</Text>
    <Text style={styles.placeholderSubtext}>В разработке...</Text>
  </View>
);

const ProfilePlaceholder = () => (
  <View style={styles.placeholder}>
    <Text style={styles.placeholderText}>Профиль пользователя</Text>
    <Text style={styles.placeholderSubtext}>В разработке...</Text>
  </View>
);

// Компонент для управления навигацией в зависимости от статуса авторизации
const AppNavigator = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563EB" />
        <Text style={styles.loadingText}>Загрузка...</Text>
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <Stack.Screen name="Dashboard" component={MainTabNavigator} />
        ) : (
          <Stack.Screen name="Login" component={LoginScreen} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

// Главный компонент приложения
export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <AppNavigator />
        <StatusBar style="auto" />
      </AuthProvider>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E2E8F0',
    paddingBottom: 34,
    paddingTop: 8,
    height: 85,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: -1,
    },
    shadowOpacity: 0.02,
    shadowRadius: 2,
    elevation: 2,
  },
  tabLabel: {
    fontSize: 12,
    fontWeight: '500',
    marginTop: 2,
    fontFamily: 'System',
    letterSpacing: -0.025,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6b7280',
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
    padding: 20,
  },
  placeholderText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  placeholderSubtext: {
    fontSize: 16,
    color: '#6b7280',
    textAlign: 'center',
  },
});
