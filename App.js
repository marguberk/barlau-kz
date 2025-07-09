import React, { useState, useEffect } from 'react';
import { StatusBar } from 'expo-status-bar';
import { View, ActivityIndicator, StyleSheet } from 'react-native';

import LoginScreen from './src/screens/LoginScreen';
import DashboardScreen from './src/screens/DashboardScreen';
import MapScreen from './src/screens/MapScreen';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [currentScreen, setCurrentScreen] = useState('dashboard');

  useEffect(() => {
    // Имитация проверки сохраненной сессии
    const checkAuthStatus = async () => {
      try {
        // Здесь можно проверить AsyncStorage для сохраненного токена
        await new Promise(resolve => setTimeout(resolve, 1000));
        setIsLoading(false);
      } catch (error) {
        console.error('Ошибка проверки авторизации:', error);
        setIsLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const handleLogin = (success) => {
    if (success) {
      setIsAuthenticated(true);
      setCurrentScreen('dashboard');
    }
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    setCurrentScreen('dashboard');
  };

  const handleNavigateToMap = () => {
    setCurrentScreen('map');
  };

  const handleBackToDashboard = () => {
    setCurrentScreen('dashboard');
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2679DB" />
      </View>
    );
  }

  const renderScreen = () => {
    if (!isAuthenticated) {
      return <LoginScreen onLogin={handleLogin} />;
    }

    switch (currentScreen) {
      case 'map':
        return <MapScreen onBack={handleBackToDashboard} />;
      case 'dashboard':
      default:
        return (
          <DashboardScreen 
            onLogout={handleLogout} 
            onNavigateToMap={handleNavigateToMap}
          />
        );
    }
  };

  return (
    <View style={styles.container}>
      {renderScreen()}
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F8FAFC',
  },
}); 
 
 
 
 