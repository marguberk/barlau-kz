import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';

export default function DashboardScreen({ onLogout, onNavigateToMap }) {
  const stats = [
    { title: 'Активные рейсы', value: '12', color: '#2679DB' },
    { title: 'Грузовики', value: '8', color: '#059669' },
    { title: 'Водители', value: '15', color: '#DC2626' },
    { title: 'Задачи', value: '23', color: '#D97706' },
  ];

  const quickActions = [
    { title: 'Новый рейс', subtitle: 'Создать новый рейс', color: '#2679DB', action: 'new_trip' },
    { title: 'Карта', subtitle: 'Отследить транспорт', color: '#059669', action: 'map' },
    { title: 'Отчеты', subtitle: 'Просмотр отчетов', color: '#7C3AED', action: 'reports' },
    { title: 'Настройки', subtitle: 'Управление системой', color: '#6B7280', action: 'settings' },
  ];

  const handleQuickAction = (action) => {
    switch (action.action) {
      case 'map':
        if (onNavigateToMap) {
          onNavigateToMap();
        } else {
          Alert.alert('Карта', 'Переход к карте транспорта');
        }
        break;
      case 'new_trip':
        Alert.alert('Новый рейс', 'Создание нового рейса');
        break;
      case 'reports':
        Alert.alert('Отчеты', 'Просмотр отчетов');
        break;
      case 'settings':
        Alert.alert('Настройки', 'Управление системой');
        break;
      default:
        Alert.alert('Действие', `Выбрано: ${action.title}`);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Добро пожаловать!</Text>
          <Text style={styles.subtitle}>BARLAU.KZ Логистика</Text>
        </View>
        <TouchableOpacity style={styles.logoutButton} onPress={onLogout}>
          <Text style={styles.logoutText}>Выйти</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Статистика</Text>
        <View style={styles.statsGrid}>
          {stats.map((stat, index) => (
            <View key={index} style={styles.statCard}>
              <Text style={[styles.statValue, { color: stat.color }]}>
                {stat.value}
              </Text>
              <Text style={styles.statTitle}>{stat.title}</Text>
            </View>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Быстрые действия</Text>
        <View style={styles.actionsGrid}>
          {quickActions.map((action, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.actionCard, { borderLeftColor: action.color }]}
              onPress={() => handleQuickAction(action)}
            >
              <Text style={styles.actionTitle}>{action.title}</Text>
              <Text style={styles.actionSubtitle}>{action.subtitle}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Последние события</Text>
        <View style={styles.eventsContainer}>
          {[
            { text: 'Рейс №1234 завершен', time: '10:30' },
            { text: 'Новый водитель добавлен', time: '09:15' },
            { text: 'Грузовик KZ123AB на техосмотре', time: '08:45' },
          ].map((event, index) => (
            <View key={index} style={styles.eventItem}>
              <Text style={styles.eventText}>{event.text}</Text>
              <Text style={styles.eventTime}>{event.time}</Text>
            </View>
          ))}
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 60,
    paddingBottom: 24,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#111827',
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
    marginTop: 4,
  },
  logoutButton: {
    backgroundColor: '#EF4444',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  logoutText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
  },
  section: {
    paddingHorizontal: 24,
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 20,
    width: '48%',
    marginBottom: 16,
    alignItems: 'center',
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  statValue: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  statTitle: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
  },
  actionsGrid: {
    gap: 12,
  },
  actionCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 20,
    borderLeftWidth: 4,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  actionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#111827',
    marginBottom: 4,
  },
  actionSubtitle: {
    fontSize: 14,
    color: '#6B7280',
  },
  eventsContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  eventItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  eventText: {
    fontSize: 16,
    color: '#111827',
    flex: 1,
  },
  eventTime: {
    fontSize: 14,
    color: '#6B7280',
  },
}); 
 
 
 
 