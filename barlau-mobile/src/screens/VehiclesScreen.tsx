import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  RefreshControl,
  Image,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { Vehicle } from '../types';
import { apiService } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Svg, Path } from 'react-native-svg';

const { width } = Dimensions.get('window');

const VehiclesScreen: React.FC = () => {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState<Vehicle | null>(null);
  const { user } = useAuth();

  const loadVehicles = async () => {
    try {
      const response = await apiService.getVehicles();
      console.log('Loaded vehicles:', response.vehicles?.length || 0);
      setVehicles(response.vehicles || []);
    } catch (error) {
      console.error('Error loading vehicles:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить список грузовиков');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadVehicles();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadVehicles();
  };

  const formatDate = (dateStr: string): string => {
    try {
      const date = new Date(dateStr);
      return date.toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return dateStr;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return (
          <Svg width={12} height={12} viewBox="0 0 12 12" fill="none">
            <Path
              d="M6 12C9.31371 12 12 9.31371 12 6C12 2.68629 9.31371 0 6 0C2.68629 0 0 2.68629 0 6C0 9.31371 2.68629 12 6 12Z"
              fill="#10B981"
            />
          </Svg>
        );
      case 'MAINTENANCE':
        return (
          <Svg width={12} height={12} viewBox="0 0 12 12" fill="none">
            <Path
              d="M6 12C9.31371 12 12 9.31371 12 6C12 2.68629 9.31371 0 6 0C2.68629 0 0 2.68629 0 6C0 9.31371 2.68629 12 6 12Z"
              fill="#F59E0B"
            />
          </Svg>
        );
      default:
        return (
          <Svg width={12} height={12} viewBox="0 0 12 12" fill="none">
            <Path
              d="M6 12C9.31371 12 12 9.31371 12 6C12 2.68629 9.31371 0 6 0C2.68629 0 0 2.68629 0 6C0 9.31371 2.68629 12 6 12Z"
              fill="#6B7280"
            />
          </Svg>
        );
    }
  };

  const closeModal = () => {
    setSelectedVehicle(null);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2563EB" />
        <Text style={styles.loadingText}>Загрузка грузовиков...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Грузовики</Text>
        <Text style={styles.subtitle}>Автопарк компании BARLAU.KZ</Text>
      </View>

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.statsContainer}>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>{vehicles.length}</Text>
            <Text style={styles.statLabel}>Всего</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>
              {vehicles.filter(v => v.status === 'ACTIVE').length}
            </Text>
            <Text style={styles.statLabel}>Активных</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statNumber}>
              {vehicles.filter(v => v.status === 'MAINTENANCE').length}
            </Text>
            <Text style={styles.statLabel}>На ТО</Text>
          </View>
        </View>

        <View style={styles.vehiclesContainer}>
          {vehicles.length === 0 ? (
            <View style={styles.emptyState}>
              <Svg width={64} height={64} viewBox="0 0 24 24" fill="none">
                <Path
                  d="M4 18H3C2.45 18 2 17.55 2 17V7C2 6.45 2.45 6 3 6H13C13.55 6 14 6.45 14 7V18H8M18 10H14V8H14.5C14.78 8 15.04 8.11 15.24 8.29C15.44 8.47 15.56 8.72 15.58 9L18 10Z"
                  stroke="#D1D5DB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  fill="none"
                />
                <Path d="M6 19C6 19 6 19 6 19C6 19 6 19 6 19" stroke="#D1D5DB" strokeWidth="2" fill="none"/>
                <Path d="M16 19C16 19 16 19 16 19C16 19 16 19 16 19" stroke="#D1D5DB" strokeWidth="2" fill="none"/>
              </Svg>
              <Text style={styles.emptyTitle}>Грузовики не найдены</Text>
              <Text style={styles.emptyText}>
                В системе пока нет зарегистрированных грузовиков
              </Text>
            </View>
          ) : (
            vehicles.map((vehicle) => (
              <TouchableOpacity
                key={vehicle.id}
                style={styles.vehicleCard}
                onPress={() => setSelectedVehicle(vehicle)}
                activeOpacity={0.7}
              >
                <View style={styles.vehicleHeader}>
                  <View style={styles.vehicleInfo}>
                    <View style={styles.vehicleTitle}>
                      <Text style={styles.vehicleBrand}>
                        {vehicle.brand} {vehicle.model}
                      </Text>
                      <View style={styles.statusContainer}>
                        {getStatusIcon(vehicle.status)}
                        <Text style={[styles.statusText, { color: vehicle.status_color }]}>
                          {vehicle.status_display}
                        </Text>
                      </View>
                    </View>
                    <Text style={styles.vehicleNumber}>{vehicle.number}</Text>
                    <Text style={styles.vehicleYear}>{vehicle.year} год</Text>
                  </View>
                  
                  {vehicle.photo ? (
                    <Image source={{ uri: vehicle.photo }} style={styles.vehicleImage} />
                  ) : (
                    <View style={styles.vehiclePlaceholder}>
                      <Svg width={40} height={40} viewBox="0 0 24 24" fill="none">
                        <Path
                          d="M4 18H3C2.45 18 2 17.55 2 17V7C2 6.45 2.45 6 3 6H13C13.55 6 14 6.45 14 7V18H8M18 10H14V8H14.5C14.78 8 15.04 8.11 15.24 8.29C15.44 8.47 15.56 8.72 15.58 9L18 10Z"
                          stroke="#9CA3AF"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          fill="none"
                        />
                        <Path d="M8 18H14" stroke="#9CA3AF" strokeWidth="2" strokeLinecap="round"/>
                      </Svg>
                    </View>
                  )}
                </View>

                <View style={styles.vehicleDetails}>
                  {vehicle.driver && (
                    <View style={styles.driverInfo}>
                      <Svg width={16} height={16} viewBox="0 0 24 24" fill="none">
                        <Path
                          d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42142 16.9217 4 17.9391 4 19V21"
                          stroke="#6B7280"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <Path
                          d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                          stroke="#6B7280"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </Svg>
                      <Text style={styles.driverText}>{vehicle.driver.name}</Text>
                    </View>
                  )}
                  
                  {vehicle.fuel_type_display && (
                    <View style={styles.fuelInfo}>
                      <Svg width={16} height={16} viewBox="0 0 24 24" fill="none">
                        <Path
                          d="M3 8L3 18C3 19.1046 3.89543 20 5 20H9C10.1046 20 11 19.1046 11 18V8H3Z"
                          stroke="#6B7280"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <Path
                          d="M7 4V8"
                          stroke="#6B7280"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                        <Path
                          d="M11 10H13L17 6V18C17 19.1046 17.8954 20 19 20C20.1046 20 21 19.1046 21 18V12L19 10"
                          stroke="#6B7280"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </Svg>
                      <Text style={styles.fuelText}>{vehicle.fuel_type_display}</Text>
                    </View>
                  )}
                </View>

                <View style={styles.vehicleFooter}>
                  <Text style={styles.vehicleType}>{vehicle.vehicle_type_display}</Text>
                  <Text style={styles.updateDate}>
                    Обновлен {formatDate(vehicle.updated_at)}
                  </Text>
                </View>
              </TouchableOpacity>
            ))
          )}
        </View>
      </ScrollView>

      {/* Модальное окно с деталями грузовика */}
      {selectedVehicle && (
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>
                {selectedVehicle.brand} {selectedVehicle.model}
              </Text>
              <TouchableOpacity onPress={closeModal} style={styles.closeButton}>
                <Svg width={24} height={24} viewBox="0 0 24 24" fill="none">
                  <Path
                    d="M18 6L6 18M6 6L18 18"
                    stroke="#6B7280"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </Svg>
              </TouchableOpacity>
            </View>

            <ScrollView style={styles.modalScroll} showsVerticalScrollIndicator={false}>
              {selectedVehicle.photo && (
                <Image source={{ uri: selectedVehicle.photo }} style={styles.modalImage} />
              )}
              
              <View style={styles.modalDetails}>
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Номер:</Text>
                  <Text style={styles.detailValue}>{selectedVehicle.number}</Text>
                </View>
                
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Год выпуска:</Text>
                  <Text style={styles.detailValue}>{selectedVehicle.year}</Text>
                </View>
                
                {selectedVehicle.color && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Цвет:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.color}</Text>
                  </View>
                )}
                
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Статус:</Text>
                  <View style={styles.statusContainer}>
                    {getStatusIcon(selectedVehicle.status)}
                    <Text style={[styles.statusText, { color: selectedVehicle.status_color }]}>
                      {selectedVehicle.status_display}
                    </Text>
                  </View>
                </View>
                
                {selectedVehicle.driver && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Водитель:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.driver.name}</Text>
                  </View>
                )}
                
                {selectedVehicle.fuel_type_display && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Тип топлива:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.fuel_type_display}</Text>
                  </View>
                )}
                
                {selectedVehicle.fuel_consumption && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Расход топлива:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.fuel_consumption} л/100км</Text>
                  </View>
                )}
                
                {selectedVehicle.cargo_capacity && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Грузоподъемность:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.cargo_capacity} кг</Text>
                  </View>
                )}
                
                {selectedVehicle.max_weight && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Макс. масса:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.max_weight} кг</Text>
                  </View>
                )}
                
                {selectedVehicle.description && (
                  <View style={styles.detailRow}>
                    <Text style={styles.detailLabel}>Описание:</Text>
                    <Text style={styles.detailValue}>{selectedVehicle.description}</Text>
                  </View>
                )}
                
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Создан:</Text>
                  <Text style={styles.detailValue}>{formatDate(selectedVehicle.created_at)}</Text>
                </View>
                
                <View style={styles.detailRow}>
                  <Text style={styles.detailLabel}>Обновлен:</Text>
                  <Text style={styles.detailValue}>{formatDate(selectedVehicle.updated_at)}</Text>
                </View>
              </View>
            </ScrollView>
          </View>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#6B7280',
  },
  header: {
    paddingHorizontal: 20,
    paddingTop: 60,
    paddingBottom: 20,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#1F2937',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
  },
  scrollView: {
    flex: 1,
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 20,
    paddingVertical: 16,
    gap: 12,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2563EB',
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 14,
    color: '#6B7280',
  },
  vehiclesContainer: {
    paddingHorizontal: 20,
    paddingBottom: 100,
  },
  vehicleCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  vehicleHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  vehicleInfo: {
    flex: 1,
  },
  vehicleTitle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 4,
  },
  vehicleBrand: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#1F2937',
    flex: 1,
  },
  vehicleNumber: {
    fontSize: 16,
    fontWeight: 'semibold',
    color: '#2563EB',
    marginBottom: 2,
  },
  vehicleYear: {
    fontSize: 14,
    color: '#6B7280',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: 'medium',
  },
  vehicleImage: {
    width: 80,
    height: 60,
    borderRadius: 8,
    backgroundColor: '#F3F4F6',
  },
  vehiclePlaceholder: {
    width: 80,
    height: 60,
    borderRadius: 8,
    backgroundColor: '#F3F4F6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  vehicleDetails: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
    marginBottom: 12,
  },
  driverInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  driverText: {
    fontSize: 14,
    color: '#374151',
  },
  fuelInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  fuelText: {
    fontSize: 14,
    color: '#374151',
  },
  vehicleFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F3F4F6',
  },
  vehicleType: {
    fontSize: 12,
    fontWeight: 'medium',
    color: '#2563EB',
    backgroundColor: '#EFF6FF',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  updateDate: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: 'semibold',
    color: '#374151',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
    paddingHorizontal: 20,
  },
  modalOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
  },
  modalContent: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    width: '100%',
    maxHeight: '80%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.25,
    shadowRadius: 20,
    elevation: 10,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#1F2937',
    flex: 1,
  },
  closeButton: {
    padding: 4,
  },
  modalScroll: {
    maxHeight: 400,
  },
  modalImage: {
    width: '100%',
    height: 200,
    backgroundColor: '#F3F4F6',
  },
  modalDetails: {
    padding: 20,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#F9FAFB',
  },
  detailLabel: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: 'medium',
  },
  detailValue: {
    fontSize: 14,
    color: '#1F2937',
    fontWeight: 'semibold',
    textAlign: 'right',
    flex: 1,
    marginLeft: 12,
  },
});

export default VehiclesScreen; 