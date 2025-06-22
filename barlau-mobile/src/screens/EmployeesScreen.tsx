import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  TouchableOpacity,
  Alert,
  Animated,
  Dimensions,
  RefreshControl,
  TextInput,
  Image,
  Modal,
  Linking,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Svg, { Path, Circle, Rect } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';
import { User } from '../types';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';

const { width } = Dimensions.get('window');

const EmployeesScreen: React.FC = () => {
  const { user } = useAuth();
  const [employees, setEmployees] = useState<User[]>([]);
  const [filteredEmployees, setFilteredEmployees] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedRole, setSelectedRole] = useState<string>('');
  const [selectedStatus, setSelectedStatus] = useState<string>('active');
  const [showFilters, setShowFilters] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState<User | null>(null);
  const [showEmployeeModal, setShowEmployeeModal] = useState(false);

  // Анимации
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(30)).current;

  // Роли для фильтрации
  const roles = [
    { value: '', label: 'Все роли' },
    { value: 'DIRECTOR', label: 'Директор' },
    { value: 'MANAGER', label: 'Менеджер' },
    { value: 'ACCOUNTANT', label: 'Бухгалтер' },
    { value: 'DRIVER', label: 'Водитель' },
    { value: 'SUPPLIER', label: 'Снабженец' },
    { value: 'TECH', label: 'Техотдел' },
  ];

  const statuses = [
    { value: 'active', label: 'Активные' },
    { value: 'archived', label: 'Архивные' },
    { value: 'all', label: 'Все' },
  ];

  useEffect(() => {
    loadEmployees();
    startAnimations();
  }, []);

  useEffect(() => {
    filterEmployees();
  }, [employees, searchQuery, selectedRole, selectedStatus]);

  const startAnimations = () => {
    Animated.parallel([
      Animated.timing(fadeAnim, {
        toValue: 1,
        duration: 800,
        useNativeDriver: true,
      }),
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 600,
        useNativeDriver: true,
      }),
    ]).start();
  };

  const loadEmployees = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getUsers();
      const employeesData = response.results || response || [];
      setEmployees(employeesData);
    } catch (error: any) {
      console.error('Ошибка загрузки сотрудников:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить список сотрудников');
    } finally {
      setIsLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadEmployees();
    setRefreshing(false);
  };

  const filterEmployees = () => {
    let filtered = [...employees];

    // Фильтр по поиску
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(emp => 
        (emp.first_name?.toLowerCase().includes(query) || '') ||
        (emp.last_name?.toLowerCase().includes(query) || '') ||
        (emp.username?.toLowerCase().includes(query) || '') ||
        (emp.email?.toLowerCase().includes(query) || '') ||
        (emp.position?.toLowerCase().includes(query) || '')
      );
    }

    // Фильтр по роли
    if (selectedRole) {
      filtered = filtered.filter(emp => emp.role === selectedRole);
    }

    // Фильтр по статусу
    if (selectedStatus === 'active') {
      filtered = filtered.filter(emp => emp.is_active && !emp.is_archived);
    } else if (selectedStatus === 'archived') {
      filtered = filtered.filter(emp => emp.is_archived);
    }

    setFilteredEmployees(filtered);
  };

  const getRoleDisplayName = (role: string) => {
    const roleMap: { [key: string]: string } = {
      'DIRECTOR': 'Директор',
      'MANAGER': 'Менеджер',
      'ACCOUNTANT': 'Бухгалтер',
      'DRIVER': 'Водитель',
      'SUPPLIER': 'Снабженец',
      'TECH': 'Техотдел',
      'SUPERADMIN': 'Суперадмин',
    };
    return roleMap[role] || role;
  };

  const getRoleBadgeColor = (role: string) => {
    const colorMap: { [key: string]: string } = {
      'DIRECTOR': '#DC2626',
      'MANAGER': '#059669',
      'ACCOUNTANT': '#16A34A',
      'DRIVER': '#2563EB',
      'SUPPLIER': '#CA8A04',
      'TECH': '#7C3AED',
      'SUPERADMIN': '#DC2626',
    };
    return colorMap[role] || '#6B7280';
  };

  const openEmployeeModal = (employee: User) => {
    setSelectedEmployee(employee);
    setShowEmployeeModal(true);
  };

  const closeEmployeeModal = () => {
    setSelectedEmployee(null);
    setShowEmployeeModal(false);
  };

  const downloadEmployeePDF = async (employee: User) => {
    try {
      Alert.alert(
        'Резюме сотрудника',
        `Хотите сгенерировать PDF резюме для ${employee.first_name} ${employee.last_name}?`,
        [
          { text: 'Отмена', style: 'cancel' },
          { 
            text: 'Генерировать', 
            onPress: async () => {
              try {
                // Показываем индикатор загрузки
                Alert.alert('Генерация PDF', 'Создаем резюме, пожалуйста подождите...');
                
                // Пытаемся скачать PDF
                await apiService.downloadEmployeePDF(employee.id);
                
                // Если дошли до сюда, значит PDF создан успешно
                Alert.alert(
                  'Резюме готово!', 
                  `PDF резюме для ${employee.first_name} ${employee.last_name} успешно создано. В мобильной версии PDF сохраняется на сервере. Полная информация доступна в карточке сотрудника.`,
                  [{ text: 'Понятно', style: 'default' }]
                );
              } catch (error: any) {
                console.error('Ошибка загрузки PDF:', error);
                if (error.response?.status === 401) {
                  Alert.alert('Ошибка', 'Нет доступа к резюме. Пожалуйста, войдите в систему заново.');
                } else if (error.response?.status === 403) {
                  Alert.alert('Ошибка', 'У вас нет прав для просмотра этого резюме.');
                } else {
                  Alert.alert('Ошибка', 'Не удалось создать резюме. Попробуйте позже.');
                }
              }
            }
          }
        ]
      );
    } catch (error) {
      console.error('Ошибка загрузки PDF:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить резюме');
    }
  };

  const EmployeeCard = ({ employee }: { employee: User }) => (
    <TouchableOpacity 
      style={styles.employeeCard}
      onPress={() => openEmployeeModal(employee)}
      activeOpacity={0.8}
    >
      <View style={styles.employeeHeader}>
        <View style={styles.employeeAvatar}>
          {employee.photo ? (
            <Image source={{ uri: employee.photo }} style={styles.avatarImage} />
          ) : (
            <Svg width={32} height={32} viewBox="0 0 24 24" fill="none">
              <Circle cx="12" cy="8" r="4" stroke="#9CA3AF" strokeWidth="2" />
              <Path
                d="M20 21C20 16.5817 16.4183 13 12 13C7.58172 13 4 16.5817 4 21"
                stroke="#9CA3AF"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </Svg>
          )}
        </View>
        <View style={styles.employeeInfo}>
          <Text style={styles.employeeName}>
            {employee.first_name && employee.last_name 
              ? `${employee.first_name} ${employee.last_name}`
              : employee.username
            }
          </Text>
          <Text style={styles.employeePosition}>
            {employee.position || getRoleDisplayName(employee.role)}
          </Text>
        </View>
        <Badge style={{ backgroundColor: getRoleBadgeColor(employee.role), color: '#FFFFFF' }}>
          {getRoleDisplayName(employee.role)}
        </Badge>
      </View>
      
      <View style={styles.employeeContacts}>
        {employee.email && (
          <View style={styles.contactItem}>
            <Svg width={16} height={16} viewBox="0 0 24 24" fill="none">
              <Path
                d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z"
                stroke="#6B7280"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="L22 6L12 13L2 6"
                stroke="#6B7280"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
            <Text style={styles.contactText}>{employee.email}</Text>
          </View>
        )}
        
        {employee.phone && (
          <View style={styles.contactItem}>
            <Svg width={16} height={16} viewBox="0 0 24 24" fill="none">
              <Path
                d="M22 16.92V19.92C22 20.52 21.52 21 20.92 21C10.93 21 3 13.07 3 3.08C3 2.48 3.48 2 4.08 2H7.09C7.69 2 8.09 2.4 8.09 3V5.5C8.09 6.1 7.69 6.5 7.09 6.5H5.09C5.09 10.9 8.69 14.5 13.09 14.5V12.5C13.09 11.9 13.49 11.5 14.09 11.5H16.59C17.19 11.5 17.59 11.9 17.59 12.5V15.5C17.59 16.1 17.19 16.5 16.59 16.5H14.59"
                stroke="#6B7280"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
            <Text style={styles.contactText}>{employee.phone}</Text>
          </View>
        )}
      </View>

      <View style={styles.employeeFooter}>
        <View style={styles.statusContainer}>
          <View style={[
            styles.statusDot, 
            { backgroundColor: employee.is_active ? '#10B981' : '#EF4444' }
          ]} />
          <Text style={styles.statusText}>
            {employee.is_active ? 'Активен' : 'Неактивен'}
          </Text>
        </View>
        
        {employee.date_joined && (
          <Text style={styles.joinDate}>
            С {new Date(employee.date_joined).toLocaleDateString('ru-RU')}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );

  const FilterButton = ({ 
    title, 
    isActive, 
    onPress 
  }: { 
    title: string; 
    isActive: boolean; 
    onPress: () => void; 
  }) => (
    <TouchableOpacity
      style={[styles.filterButton, isActive && styles.filterButtonActive]}
      onPress={onPress}
    >
      <Text style={[styles.filterButtonText, isActive && styles.filterButtonTextActive]}>
        {title}
      </Text>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <Animated.View 
        style={[
          styles.content,
          {
            opacity: fadeAnim,
            transform: [{ translateY: slideAnim }],
          },
        ]}
      >
        {/* Заголовок */}
        <View style={styles.header}>
          <Text style={styles.title}>Сотрудники</Text>
          <TouchableOpacity
            style={styles.filterToggle}
            onPress={() => setShowFilters(!showFilters)}
          >
            <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
              <Path
                d="M22 3H2L10 12.46V19L14 21V12.46L22 3Z"
                stroke="#6B7280"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </TouchableOpacity>
        </View>

        {/* Поиск */}
        <View style={styles.searchContainer}>
          <Svg width={20} height={20} viewBox="0 0 24 24" fill="none" style={styles.searchIcon}>
            <Circle cx="11" cy="11" r="8" stroke="#9CA3AF" strokeWidth="2" />
            <Path d="M21 21L16.65 16.65" stroke="#9CA3AF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </Svg>
          <TextInput
            style={styles.searchInput}
            placeholder="Поиск по имени, email..."
            value={searchQuery}
            onChangeText={setSearchQuery}
            placeholderTextColor="#9CA3AF"
          />
        </View>

        {/* Фильтры */}
        {showFilters && (
          <View style={styles.filtersContainer}>
            <Text style={styles.filterLabel}>Роль:</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
              {roles.map((role) => (
                <FilterButton
                  key={role.value}
                  title={role.label}
                  isActive={selectedRole === role.value}
                  onPress={() => setSelectedRole(role.value)}
                />
              ))}
            </ScrollView>

            <Text style={styles.filterLabel}>Статус:</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterScroll}>
              {statuses.map((status) => (
                <FilterButton
                  key={status.value}
                  title={status.label}
                  isActive={selectedStatus === status.value}
                  onPress={() => setSelectedStatus(status.value)}
                />
              ))}
            </ScrollView>
          </View>
        )}

        {/* Статистика */}
        <View style={styles.statsContainer}>
          <Text style={styles.statsText}>
            Найдено: {filteredEmployees.length} из {employees.length}
          </Text>
        </View>

        {/* Список сотрудников */}
        <ScrollView
          style={styles.scrollView}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          showsVerticalScrollIndicator={false}
        >
          {isLoading ? (
            <View style={styles.loadingContainer}>
              <Text style={styles.loadingText}>Загрузка сотрудников...</Text>
            </View>
          ) : filteredEmployees.length === 0 ? (
            <View style={styles.emptyContainer}>
              <Svg width={64} height={64} viewBox="0 0 24 24" fill="none">
                <Path
                  d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21"
                  stroke="#D1D5DB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <Circle cx="9" cy="7" r="4" stroke="#D1D5DB" strokeWidth="2" />
                <Path
                  d="M23 21V19C23 18.1645 22.7155 17.3541 22.2094 16.6972C21.7033 16.0403 20.9991 15.5731 20.2 15.36"
                  stroke="#D1D5DB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <Path
                  d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1018 4.55232C18.5806 5.25392 18.7492 6.11683 18.5775 6.95013C18.4058 7.78342 17.9047 8.52234 17.1849 9.01114C16.4651 9.49994 15.5808 9.70928 14.72 9.6"
                  stroke="#D1D5DB"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </Svg>
              <Text style={styles.emptyText}>Сотрудники не найдены</Text>
              <Text style={styles.emptySubtext}>
                Попробуйте изменить параметры поиска
              </Text>
            </View>
          ) : (
            <View style={styles.employeesList}>
              {filteredEmployees.map((employee) => (
                <EmployeeCard key={employee.id} employee={employee} />
              ))}
            </View>
          )}
        </ScrollView>
      </Animated.View>

      {/* Модальное окно с детальной информацией */}
      <Modal
        visible={showEmployeeModal}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={closeEmployeeModal}
      >
        <SafeAreaView style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Информация о сотруднике</Text>
            <TouchableOpacity onPress={closeEmployeeModal}>
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

          {selectedEmployee && (
            <ScrollView style={styles.modalContent}>
              {/* Заголовок профиля */}
              <View style={styles.modalEmployeeHeader}>
                <View style={styles.modalAvatar}>
                  {selectedEmployee.photo ? (
                    <Image source={{ uri: selectedEmployee.photo }} style={styles.modalAvatarImage} />
                  ) : (
                    <View style={styles.avatarPlaceholder}>
                      <Text style={styles.avatarPlaceholderText}>
                        {selectedEmployee.first_name?.[0] || ''}{selectedEmployee.last_name?.[0] || ''}
                      </Text>
                    </View>
                  )}
                </View>
                <Text style={styles.modalEmployeeName}>
                  {selectedEmployee.first_name && selectedEmployee.last_name 
                    ? `${selectedEmployee.first_name} ${selectedEmployee.last_name}`
                    : selectedEmployee.username
                  }
                </Text>
                <Text style={styles.modalEmployeePosition}>
                  {selectedEmployee.position || getRoleDisplayName(selectedEmployee.role)}
                </Text>
                <Badge style={{ backgroundColor: getRoleBadgeColor(selectedEmployee.role), color: '#FFFFFF', marginTop: 8 }}>
                  {getRoleDisplayName(selectedEmployee.role)}
                </Badge>
                
                {/* Кнопка загрузки PDF */}
                <TouchableOpacity 
                  style={styles.downloadButton}
                  onPress={() => downloadEmployeePDF(selectedEmployee)}
                >
                  <Svg width={16} height={16} viewBox="0 0 24 24" fill="none">
                    <Path
                      d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15"
                      stroke="white"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <Path
                      d="M7 10L12 15L17 10"
                      stroke="white"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                    <Path
                      d="M12 15V3"
                      stroke="white"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </Svg>
                  <Text style={styles.downloadButtonText}>Скачать резюме PDF</Text>
                </TouchableOpacity>
              </View>

              {/* Контактная информация */}
              <View style={styles.modalSection}>
                <Text style={styles.modalSectionTitle}>Контактная информация</Text>
                
                {selectedEmployee.email && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path
                        d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z"
                        stroke="#6B7280"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                      <Path
                        d="L22 6L12 13L2 6"
                        stroke="#6B7280"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </Svg>
                    <Text style={styles.modalInfoText}>{selectedEmployee.email}</Text>
                  </View>
                )}

                {selectedEmployee.phone && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path
                        d="M22 16.92V19.92C22 20.52 21.52 21 20.92 21C10.93 21 3 13.07 3 3.08C3 2.48 3.48 2 4.08 2H7.09C7.69 2 8.09 2.4 8.09 3V5.5C8.09 6.1 7.69 6.5 7.09 6.5H5.09C5.09 10.9 8.69 14.5 13.09 14.5V12.5C13.09 11.9 13.49 11.5 14.09 11.5H16.59C17.19 11.5 17.59 11.9 17.59 12.5V15.5C17.59 16.1 17.19 16.5 16.59 16.5H14.59"
                        stroke="#6B7280"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      />
                    </Svg>
                    <Text style={styles.modalInfoText}>{selectedEmployee.phone}</Text>
                  </View>
                )}
              </View>

              {/* О себе */}
              {selectedEmployee.experience && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Опыт работы</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.experience}</Text>
                </View>
              )}

              {/* Образование */}
              {selectedEmployee.education && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Образование</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.education}</Text>
                </View>
              )}

              {/* Навыки */}
              {selectedEmployee.skills && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Навыки</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.skills}</Text>
                </View>
              )}

              {/* Информация о работе */}
              <View style={styles.modalSection}>
                <Text style={styles.modalSectionTitle}>Информация о работе</Text>
                
                <View style={styles.modalInfoRow}>
                  <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                    <Rect x="2" y="3" width="20" height="14" rx="2" ry="2" stroke="#6B7280" strokeWidth="2" />
                    <Path d="M8 21L12 17L16 21" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </Svg>
                  <Text style={styles.modalInfoText}>
                    {selectedEmployee.position || getRoleDisplayName(selectedEmployee.role)}
                  </Text>
                </View>

                {selectedEmployee.date_joined && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="#6B7280" strokeWidth="2" />
                      <Path d="M16 2V6M8 2V6M3 10H21" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </Svg>
                    <Text style={styles.modalInfoText}>
                      Работает с {new Date(selectedEmployee.date_joined).toLocaleDateString('ru-RU')}
                    </Text>
                  </View>
                )}

                <View style={styles.modalInfoRow}>
                  <View style={[
                    styles.statusDot, 
                    { backgroundColor: selectedEmployee.is_active ? '#10B981' : '#EF4444' }
                  ]} />
                  <Text style={styles.modalInfoText}>
                    {selectedEmployee.is_active ? 'Активный сотрудник' : 'Неактивный сотрудник'}
                  </Text>
                </View>
              </View>

              {/* О себе */}
              {selectedEmployee.about_me && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>О себе</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.about_me}</Text>
                </View>
              )}

              {/* Ключевые навыки */}
              {selectedEmployee.key_skills && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Ключевые навыки</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.key_skills}</Text>
                </View>
              )}

              {/* Сертификаты */}
              {selectedEmployee.certifications && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Сертификаты</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.certifications}</Text>
                </View>
              )}

              {/* Языки */}
              {selectedEmployee.languages && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Языки</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.languages}</Text>
                </View>
              )}

              {/* Достижения */}
              {selectedEmployee.achievements && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Достижения</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.achievements}</Text>
                </View>
              )}

              {/* Курсы */}
              {selectedEmployee.courses && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Курсы и обучение</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.courses}</Text>
                </View>
              )}

              {/* Публикации */}
              {selectedEmployee.publications && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Публикации</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.publications}</Text>
                </View>
              )}

              {/* Хобби */}
              {selectedEmployee.hobbies && (
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Хобби и интересы</Text>
                  <Text style={styles.modalSectionText}>{selectedEmployee.hobbies}</Text>
                </View>
              )}

              {/* Дополнительная информация */}
              <View style={styles.modalSection}>
                <Text style={styles.modalSectionTitle}>Дополнительная информация</Text>
                
                {selectedEmployee.age && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Circle cx="12" cy="12" r="10" stroke="#6B7280" strokeWidth="2" />
                      <Path d="M12 6V12L16 14" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </Svg>
                    <Text style={styles.modalInfoText}>Возраст: {selectedEmployee.age} лет</Text>
                  </View>
                )}

                {selectedEmployee.desired_salary && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path d="M12 1V23M17 5H9.5C8.11929 5 7 6.11929 7 7.5S8.11929 10 9.5 10H14.5C15.8807 10 17 11.1193 17 12.5S15.8807 15 14.5 15H7" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </Svg>
                    <Text style={styles.modalInfoText}>
                      Желаемая зарплата: {selectedEmployee.desired_salary?.toLocaleString('ru-RU')} тенге
                    </Text>
                  </View>
                )}

                {selectedEmployee.location && (
                  <View style={styles.modalInfoRow}>
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path d="M21 10C21 17 12 23 12 23S3 17 3 10C3 5.02944 7.02944 1 12 1C16.9706 1 21 5.02944 21 10Z" stroke="#6B7280" strokeWidth="2" />
                      <Circle cx="12" cy="10" r="3" stroke="#6B7280" strokeWidth="2" />
                    </Svg>
                    <Text style={styles.modalInfoText}>{selectedEmployee.location}</Text>
                  </View>
                )}

                {selectedEmployee.linkedin && (
                  <TouchableOpacity 
                    style={styles.modalInfoRow}
                    onPress={() => Linking.openURL(selectedEmployee.linkedin!)}
                  >
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path d="M16 8C18.2091 8 20 9.79086 20 12V21H16V12C16 11.4477 15.5523 11 15 11C14.4477 11 14 11.4477 14 12V21H10V12C10 9.79086 11.7909 8 14 8H16Z" stroke="#0077B5" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      <Rect x="2" y="9" width="4" height="12" stroke="#0077B5" strokeWidth="2" />
                      <Circle cx="4" cy="4" r="2" stroke="#0077B5" strokeWidth="2" />
                    </Svg>
                    <Text style={[styles.modalInfoText, { color: '#0077B5' }]}>LinkedIn профиль</Text>
                  </TouchableOpacity>
                )}

                {selectedEmployee.portfolio_url && (
                  <TouchableOpacity 
                    style={styles.modalInfoRow}
                    onPress={() => Linking.openURL(selectedEmployee.portfolio_url!)}
                  >
                    <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
                      <Path d="M10 13C10.4295 13.5741 10.9774 14.0491 11.6066 14.3929C12.2357 14.7367 12.9315 14.9411 13.6467 14.9923C14.3618 15.0435 15.0796 14.9403 15.7513 14.6897C16.4231 14.4392 17.0331 14.047 17.54 13.54L20.54 10.54C21.4508 9.59695 21.9548 8.33394 21.9434 7.02296C21.932 5.71198 21.4061 4.45791 20.4791 3.53087C19.5521 2.60383 18.298 2.07799 16.987 2.0666C15.676 2.0552 14.413 2.55918 13.47 3.47L11.75 5.18" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                      <Path d="M14 11C13.5705 10.4259 13.0226 9.95085 12.3934 9.60706C11.7643 9.26327 11.0685 9.05891 10.3533 9.00769C9.63819 8.95646 8.92037 9.05969 8.24864 9.31025C7.5769 9.56082 6.9669 9.95301 6.46 10.46L3.46 13.46C2.54918 14.403 2.04520 15.6661 2.05660 16.977C2.068 18.288 2.59384 19.5421 3.52088 20.4691C4.44792 21.3962 5.70199 21.922 7.01297 21.9334C8.32395 21.9448 9.58696 21.4408 10.53 20.53L12.24 18.82" stroke="#6B7280" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </Svg>
                    <Text style={[styles.modalInfoText, { color: '#2563EB' }]}>Портфолио</Text>
                  </TouchableOpacity>
                )}
              </View>
            </ScrollView>
          )}
        </SafeAreaView>
      </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  content: {
    flex: 1,
    paddingHorizontal: 16,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 20,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#0F172A',
  },
  filterToggle: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: '#FFFFFF',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 12,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  searchIcon: {
    marginRight: 12,
  },
  searchInput: {
    flex: 1,
    fontSize: 16,
    color: '#0F172A',
  },
  filtersContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  filterLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: '#374151',
    marginBottom: 8,
    marginTop: 8,
  },
  filterScroll: {
    marginBottom: 8,
  },
  filterButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: '#F3F4F6',
    marginRight: 8,
  },
  filterButtonActive: {
    backgroundColor: '#2563EB',
  },
  filterButtonText: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: '500',
  },
  filterButtonTextActive: {
    color: '#FFFFFF',
  },
  statsContainer: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  statsText: {
    fontSize: 14,
    color: '#6B7280',
    fontWeight: '500',
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    padding: 40,
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#6B7280',
  },
  emptyContainer: {
    padding: 40,
    alignItems: 'center',
  },
  emptyText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#6B7280',
    marginTop: 16,
  },
  emptySubtext: {
    fontSize: 14,
    color: '#9CA3AF',
    marginTop: 8,
    textAlign: 'center',
  },
  employeesList: {
    paddingBottom: 20,
  },
  employeeCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  employeeHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  employeeAvatar: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#F3F4F6',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
    overflow: 'hidden',
  },
  avatarImage: {
    width: 48,
    height: 48,
    borderRadius: 24,
  },
  employeeInfo: {
    flex: 1,
  },
  employeeName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#0F172A',
    marginBottom: 2,
  },
  employeePosition: {
    fontSize: 14,
    color: '#6B7280',
  },
  employeeContacts: {
    marginBottom: 12,
  },
  contactItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
  },
  contactText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 8,
  },
  employeeFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#F3F4F6',
  },
  statusContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  statusText: {
    fontSize: 12,
    color: '#6B7280',
    fontWeight: '500',
  },
  joinDate: {
    fontSize: 12,
    color: '#9CA3AF',
  },
  // Модальное окно
  modalContainer: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
    backgroundColor: '#FFFFFF',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#0F172A',
  },
  modalContent: {
    flex: 1,
    padding: 16,
  },
  modalEmployeeHeader: {
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 24,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  modalAvatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#F3F4F6',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 16,
    overflow: 'hidden',
  },
  modalAvatarImage: {
    width: 80,
    height: 80,
    borderRadius: 40,
  },
  modalEmployeeName: {
    fontSize: 20,
    fontWeight: '700',
    color: '#0F172A',
    marginBottom: 8,
    textAlign: 'center',
  },
  modalSection: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.06,
    shadowRadius: 4,
    elevation: 2,
  },
  modalSectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#0F172A',
    marginBottom: 12,
  },
  modalInfoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  modalInfoText: {
    fontSize: 14,
    color: '#6B7280',
    marginLeft: 12,
    flex: 1,
  },
  avatarPlaceholder: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: '#2563EB',
    alignItems: 'center',
    justifyContent: 'center',
  },
  avatarPlaceholderText: {
    fontSize: 24,
    fontWeight: '700',
    color: '#FFFFFF',
  },
  modalEmployeePosition: {
    fontSize: 16,
    color: '#6B7280',
    marginBottom: 8,
    textAlign: 'center',
  },
  downloadButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#2563EB',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 8,
    marginTop: 16,
  },
  downloadButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 8,
  },
  modalSectionText: {
    fontSize: 14,
    color: '#374151',
    lineHeight: 20,
  },
});

export default EmployeesScreen;