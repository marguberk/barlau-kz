import React from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
} from 'react-native';

export default function MapScreen({ onBack }) {
  const vehicles = [
    { id: 'KZ123AB', driver: 'Иванов И.И.', status: 'В пути', location: 'Алматы → Астана' },
    { id: 'KZ456CD', driver: 'Петров П.П.', status: 'Загрузка', location: 'Склад №1' },
    { id: 'KZ789EF', driver: 'Сидоров С.С.', status: 'Разгрузка', location: 'Склад №3' },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'В пути': return '#2679DB';
      case 'Загрузка': return '#D97706';
      case 'Разгрузка': return '#059669';
      default: return '#6B7280';
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backButton} onPress={onBack}>
          <Text style={styles.backButtonText}>← Назад</Text>
        </TouchableOpacity>
        <Text style={styles.title}>Карта транспорта</Text>
        <View style={styles.placeholder} />
      </View>

      <View style={styles.mapContainer}>
        <View style={styles.mapPlaceholder}>
          <Text style={styles.mapPlaceholderText}>🗺️</Text>
          <Text style={styles.mapPlaceholderSubtext}>
            Здесь будет интерактивная карта{'\n'}с отслеживанием транспорта
          </Text>
        </View>
      </View>

      <View style={styles.vehiclesList}>
        <Text style={styles.sectionTitle}>Активный транспорт</Text>
        <ScrollView style={styles.scrollView}>
          {vehicles.map((vehicle, index) => (
            <View key={index} style={styles.vehicleCard}>
              <View style={styles.vehicleHeader}>
                <Text style={styles.vehicleId}>{vehicle.id}</Text>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor(vehicle.status) }]}>
                  <Text style={styles.statusText}>{vehicle.status}</Text>
                </View>
              </View>
              <Text style={styles.driverName}>{vehicle.driver}</Text>
              <Text style={styles.location}>{vehicle.location}</Text>
            </View>
          ))}
        </ScrollView>
      </View>
    </View>
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
    paddingBottom: 16,
  },
  backButton: {
    paddingVertical: 8,
    paddingHorizontal: 12,
  },
  backButtonText: {
    fontSize: 16,
    color: '#2679DB',
    fontWeight: '600',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#111827',
  },
  placeholder: {
    width: 50,
  },
  mapContainer: {
    flex: 1,
    margin: 16,
    borderRadius: 12,
    overflow: 'hidden',
  },
  mapPlaceholder: {
    flex: 1,
    backgroundColor: '#E5E7EB',
    justifyContent: 'center',
    alignItems: 'center',
  },
  mapPlaceholderText: {
    fontSize: 48,
    marginBottom: 16,
  },
  mapPlaceholderSubtext: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
    lineHeight: 24,
  },
  vehiclesList: {
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    paddingTop: 24,
    paddingHorizontal: 24,
    maxHeight: 300,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 16,
  },
  scrollView: {
    flex: 1,
  },
  vehicleCard: {
    backgroundColor: '#F9FAFB',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#2679DB',
  },
  vehicleHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  vehicleId: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  statusText: {
    color: '#FFFFFF',
    fontSize: 12,
    fontWeight: '600',
  },
  driverName: {
    fontSize: 16,
    color: '#374151',
    marginBottom: 4,
  },
  location: {
    fontSize: 14,
    color: '#6B7280',
  },
}); 
 
 
 
 