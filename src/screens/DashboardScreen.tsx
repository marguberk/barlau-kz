import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '../context/AuthContext';
import ApiService from '../services/api';

const DashboardScreen = () => {
  const { user, logout } = useAuth();
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [stats, setStats] = useState({
    activeTrips: 0,
    totalVehicles: 0,
    totalEmployees: 0,
    pendingTasks: 0,
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      // Загружаем данные параллельно
      const [trips, vehicles, employees, tasks] = await Promise.allSettled([
        ApiService.getTrips(),
        ApiService.getVehicles(),
        ApiService.getEmployees(),
        ApiService.getTasks(),
      ]);

      setStats({
        activeTrips: trips.status === 'fulfilled' ? trips.value.filter(trip => trip.status === 'active').length : 0,
        totalVehicles: vehicles.status === 'fulfilled' ? vehicles.value.length : 0,
        totalEmployees: employees.status === 'fulfilled' ? employees.value.length : 0,
        pendingTasks: tasks.status === 'fulfilled' ? tasks.value.filter(task => task.status === 'pending').length : 0,
      });
    } catch (error) {
      console.error('Dashboard data loading error:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить данные');
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setIsRefreshing(true);
    await loadDashboardData();
    setIsRefreshing(false);
  };

  const handleLogout = () => {
    Alert.alert(
      'Выход',
      'Вы уверены, что хотите выйти из системы?',
      [
        { text: 'Отмена', style: 'cancel' },
        { text: 'Выйти', style: 'destructive', onPress: logout },
      ]
    );
  };

  if (isLoading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#2679DB" />
          <Text style={styles.loadingText}>Загрузка...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
        }
      >
        {/* Заголовок */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Добро пожаловать,</Text>
            <Text style={styles.userName}>
              {user?.first_name} {user?.last_name}
            </Text>
          </View>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Text style={styles.logoutButtonText}>Выйти</Text>
          </TouchableOpacity>
        </View>

        {/* Статистические карточки */}
        <View style={styles.statsContainer}>
          <View style={styles.statsRow}>
            <View style={[styles.statCard, styles.statCardPrimary]}>
              <Text style={styles.statNumber}>{stats.activeTrips}</Text>
              <Text style={styles.statLabel}>Активные поездки</Text>
            </View>
            <View style={[styles.statCard, styles.statCardSecondary]}>
              <Text style={styles.statNumber}>{stats.pendingTasks}</Text>
              <Text style={styles.statLabel}>Задачи в ожидании</Text>
            </View>
          </View>
          <View style={styles.statsRow}>
            <View style={[styles.statCard, styles.statCardAccent]}>
              <Text style={styles.statNumber}>{stats.totalVehicles}</Text>
              <Text style={styles.statLabel}>Всего грузовиков</Text>
            </View>
            <View style={[styles.statCard, styles.statCardNeutral]}>
              <Text style={styles.statNumber}>{stats.totalEmployees}</Text>
              <Text style={styles.statLabel}>Сотрудников</Text>
            </View>
          </View>
        </View>

        {/* Быстрые действия */}
        <View style={styles.quickActionsContainer}>
          <Text style={styles.sectionTitle}>Быстрые действия</Text>
          <View style={styles.quickActionsGrid}>
            <TouchableOpacity style={styles.quickActionCard}>
              <Text style={styles.quickActionIcon}>🗺️</Text>
              <Text style={styles.quickActionText}>Карта</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.quickActionCard}>
              <Text style={styles.quickActionIcon}>📋</Text>
              <Text style={styles.quickActionText}>Задачи</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.quickActionCard}>
              <Text style={styles.quickActionIcon}>🚛</Text>
              <Text style={styles.quickActionText}>Грузовики</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.quickActionCard}>
              <Text style={styles.quickActionIcon}>👥</Text>
              <Text style={styles.quickActionText}>Сотрудники</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Последние обновления */}
        <View style={styles.updatesContainer}>
          <Text style={styles.sectionTitle}>Последние обновления</Text>
          <View style={styles.updateCard}>
            <Text style={styles.updateText}>
              Система работает в штатном режиме
            </Text>
            <Text style={styles.updateTime}>Обновлено сейчас</Text>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6B7280',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 20,
  },
  greeting: {
    fontSize: 16,
    color: '#6B7280',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#111827',
    marginTop: 4,
  },
  logoutButton: {
    backgroundColor: '#EF4444',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  logoutButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '500',
  },
  statsContainer: {
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  statsRow: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  statCard: {
    flex: 1,
    padding: 20,
    borderRadius: 16,
    marginHorizontal: 4,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  statCardPrimary: {
    backgroundColor: '#2679DB',
  },
  statCardSecondary: {
    backgroundColor: '#10B981',
  },
  statCardAccent: {
    backgroundColor: '#F59E0B',
  },
  statCardNeutral: {
    backgroundColor: '#6B7280',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  quickActionsContainer: {
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 16,
  },
  quickActionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  quickActionCard: {
    width: '48%',
    backgroundColor: '#FFFFFF',
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    marginBottom: 12,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  quickActionIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  quickActionText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
  },
  updatesContainer: {
    paddingHorizontal: 20,
    marginBottom: 24,
  },
  updateCard: {
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    shadowColor: '#000000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  updateText: {
    fontSize: 16,
    color: '#374151',
    marginBottom: 4,
  },
  updateTime: {
    fontSize: 12,
    color: '#9CA3AF',
  },
});

export default DashboardScreen; 
 
 
 
 