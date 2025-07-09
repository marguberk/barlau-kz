import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  Alert,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';

type Screen = 'login' | 'dashboard' | 'tasks' | 'map' | 'vehicles' | 'employees';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (username === 'admin' && password === 'password') {
      setCurrentScreen('dashboard');
    } else {
      Alert.alert('Ошибка', 'Неверный логин или пароль\nИспользуйте: admin / password');
    }
  };

  const handleLogout = () => {
    setCurrentScreen('login');
    setUsername('');
    setPassword('');
  };

  const TabButton = ({ title, screen, active }: { title: string; screen: Screen; active: boolean }) => (
    <TouchableOpacity
      style={[styles.tabButton, active && styles.tabButtonActive]}
      onPress={() => setCurrentScreen(screen)}
    >
      <Text style={[styles.tabText, active && styles.tabTextActive]}>{title}</Text>
    </TouchableOpacity>
  );

  if (currentScreen === 'login') {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loginContainer}>
          <View style={styles.logoContainer}>
            <Text style={styles.logoText}>BARLAU.KZ</Text>
            <Text style={styles.subtitle}>Система управления логистикой</Text>
          </View>

          <View style={styles.formContainer}>
            <TextInput
              style={styles.input}
              placeholder="Логин"
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />
            <TextInput
              style={styles.input}
              placeholder="Пароль"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoCapitalize="none"
            />
            <TouchableOpacity style={styles.loginButton} onPress={handleLogin}>
              <Text style={styles.loginButtonText}>Войти</Text>
            </TouchableOpacity>
          </View>

          <Text style={styles.hint}>Демо: admin / password</Text>
        </View>
        <StatusBar style="auto" />
      </SafeAreaView>
    );
  }

  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard':
        return (
          <ScrollView style={styles.content}>
            <View style={styles.header}>
              <Text style={styles.title}>Дашборд</Text>
              <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
                <Text style={styles.logoutText}>Выйти</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.statsContainer}>
              <View style={styles.statCard}>
                <Text style={styles.statNumber}>12</Text>
                <Text style={styles.statLabel}>Активные рейсы</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={styles.statNumber}>45</Text>
                <Text style={styles.statLabel}>Грузовики</Text>
              </View>
            </View>

            <View style={styles.statsContainer}>
              <View style={styles.statCard}>
                <Text style={styles.statNumber}>28</Text>
                <Text style={styles.statLabel}>Водители</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={styles.statNumber}>8</Text>
                <Text style={styles.statLabel}>Задачи</Text>
              </View>
            </View>

            <View style={styles.sectionContainer}>
              <Text style={styles.sectionTitle}>Последние обновления</Text>
              <View style={styles.updateItem}>
                <Text style={styles.updateText}>Рейс #003KZ777 завершен</Text>
                <Text style={styles.updateTime}>2 часа назад</Text>
              </View>
              <View style={styles.updateItem}>
                <Text style={styles.updateText}>Новый водитель добавлен</Text>
                <Text style={styles.updateTime}>4 часа назад</Text>
              </View>
              <View style={styles.updateItem}>
                <Text style={styles.updateText}>Грузовик MAN в пути</Text>
                <Text style={styles.updateTime}>6 часов назад</Text>
              </View>
            </View>
          </ScrollView>
        );
      default:
        return (
          <View style={styles.placeholderContainer}>
            <Text style={styles.placeholderTitle}>
              {currentScreen === 'tasks' && 'Задачи'}
              {currentScreen === 'map' && 'Карта'}
              {currentScreen === 'vehicles' && 'Грузовики'}
              {currentScreen === 'employees' && 'Сотрудники'}
            </Text>
            <Text style={styles.placeholderText}>В разработке...</Text>
          </View>
        );
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {renderScreen()}
      
      <View style={styles.tabContainer}>
        <TabButton title="Главная" screen="dashboard" active={currentScreen === 'dashboard'} />
        <TabButton title="Задачи" screen="tasks" active={currentScreen === 'tasks'} />
        <TabButton title="Карта" screen="map" active={currentScreen === 'map'} />
        <TabButton title="Грузовики" screen="vehicles" active={currentScreen === 'vehicles'} />
        <TabButton title="Сотрудники" screen="employees" active={currentScreen === 'employees'} />
      </View>
      <StatusBar style="auto" />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  loginContainer: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 32,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 48,
  },
  logoText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2679DB',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    textAlign: 'center',
  },
  formContainer: {
    marginBottom: 24,
  },
  input: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#e2e8f0',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 16,
    marginBottom: 16,
  },
  loginButton: {
    backgroundColor: '#2679DB',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  loginButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  hint: {
    textAlign: 'center',
    color: '#64748b',
    fontSize: 14,
    fontStyle: 'italic',
  },
  content: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: '#ffffff',
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
  },
  logoutButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: '#ef4444',
    borderRadius: 8,
  },
  logoutText: {
    color: '#ffffff',
    fontSize: 14,
    fontWeight: '500',
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    paddingTop: 20,
    gap: 16,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#ffffff',
    padding: 20,
    borderRadius: 12,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2679DB',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 14,
    color: '#64748b',
    textAlign: 'center',
  },
  sectionContainer: {
    margin: 20,
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1f2937',
    marginBottom: 16,
  },
  updateItem: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#f1f5f9',
  },
  updateText: {
    fontSize: 16,
    color: '#374151',
    marginBottom: 4,
  },
  updateTime: {
    fontSize: 12,
    color: '#9ca3af',
  },
  placeholderContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  placeholderTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1f2937',
    marginBottom: 8,
  },
  placeholderText: {
    fontSize: 16,
    color: '#6b7280',
  },
  tabContainer: {
    flexDirection: 'row',
    backgroundColor: '#ffffff',
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    paddingBottom: 34,
    paddingTop: 8,
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 8,
  },
  tabButtonActive: {
    backgroundColor: '#f0f9ff',
  },
  tabText: {
    fontSize: 12,
    color: '#64748b',
    fontWeight: '500',
  },
  tabTextActive: {
    color: '#2679DB',
    fontWeight: '600',
  },
}); 