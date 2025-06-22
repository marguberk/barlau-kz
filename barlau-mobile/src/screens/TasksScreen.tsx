import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  RefreshControl,
  SafeAreaView,
  Alert,
  Modal,
} from 'react-native';
import Svg, { Path } from 'react-native-svg';
import { useAuth } from '../context/AuthContext';
import { Task } from '../types';
import apiService from '../services/api';
import Card from '../components/Card';
import Badge from '../components/Badge';
import Button from '../components/Button';

interface TasksByStatus {
  NEW: Task[];
  IN_PROGRESS: Task[];
  COMPLETED: Task[];
  CANCELLED: Task[];
}

const TasksScreen: React.FC = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [tasksByStatus, setTasksByStatus] = useState<TasksByStatus>({
    NEW: [],
    IN_PROGRESS: [],
    COMPLETED: [],
    CANCELLED: [],
  });
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [isModalVisible, setIsModalVisible] = useState(false);

  useEffect(() => {
    loadTasks();
  }, []);

  useEffect(() => {
    groupTasksByStatus();
  }, [tasks]);

  const loadTasks = async () => {
    try {
      setIsLoading(true);
      const response = await apiService.getTasks();
      setTasks(response.results || []);
    } catch (error) {
      console.error('Ошибка загрузки задач:', error);
      Alert.alert('Ошибка', 'Не удалось загрузить задачи');
    } finally {
      setIsLoading(false);
    }
  };

  const groupTasksByStatus = () => {
    const grouped: TasksByStatus = {
      NEW: [],
      IN_PROGRESS: [],
      COMPLETED: [],
      CANCELLED: [],
    };

    tasks.forEach(task => {
      if (grouped[task.status as keyof TasksByStatus]) {
        grouped[task.status as keyof TasksByStatus].push(task);
      }
    });

    setTasksByStatus(grouped);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadTasks();
    setRefreshing(false);
  };

  const updateTaskStatus = async (taskId: number, newStatus: Task['status']) => {
    try {
      await apiService.updateTaskStatus(taskId, newStatus);
      
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? { ...task, status: newStatus } : task
        )
      );

      Alert.alert('Успешно', 'Статус задачи обновлен');
      setIsModalVisible(false);
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
      Alert.alert('Ошибка', 'Не удалось обновить статус задачи');
    }
  };

  const getStatusTitle = (status: string) => {
    const titles = {
      NEW: 'К выполнению',
      IN_PROGRESS: 'В работе',
      COMPLETED: 'Выполнено',
      CANCELLED: 'Отменено',
    };
    return titles[status as keyof typeof titles] || status;
  };

  const getStatusBadgeVariant = (status: string): 'default' | 'secondary' | 'destructive' | 'outline' => {
    const variants = {
      NEW: 'outline' as const,
      IN_PROGRESS: 'secondary' as const,
      COMPLETED: 'default' as const,
      CANCELLED: 'destructive' as const,
    };
    return variants[status as keyof typeof variants] || 'outline';
  };

  const renderTaskItem = (task: Task, status: string) => (
    <Card 
      key={task.id}
      style={styles.taskCard}
      onPress={() => {
        setSelectedTask(task);
        setIsModalVisible(true);
      }}
    >
      <Card.Content style={styles.taskContent}>
        <View style={styles.taskHeader}>
          <Text style={styles.taskTitle}>{task.title}</Text>
          <Badge variant={getStatusBadgeVariant(status)}>
            {getStatusTitle(status)}
          </Badge>
        </View>
        
        <Text style={styles.taskDescription} numberOfLines={2}>
          {task.description}
        </Text>
        
        <View style={styles.taskFooter}>
          <View style={styles.taskMeta}>
            <Svg width={14} height={14} viewBox="0 0 24 24" fill="none" style={styles.metaIcon}>
              <Path
                d="M8 2V6"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M16 2V6"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M3.5 9.09H20.5"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M21 8.5V17C21 20 19.5 22 16 22H8C4.5 22 3 20 3 17V8.5C3 5.5 4.5 3.5 8 3.5H16C19.5 3.5 21 5.5 21 8.5Z"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
            <Text style={styles.metaText}>
              {new Date(task.due_date).toLocaleDateString('ru-RU', {
                day: '2-digit',
                month: 'short'
              })}
            </Text>
          </View>
          
          {task.assigned_to && (
            <View style={styles.taskMeta}>
              <Svg width={14} height={14} viewBox="0 0 24 24" fill="none" style={styles.metaIcon}>
                <Path
                  d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
                  stroke="#64748B"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <Path
                  d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                  stroke="#64748B"
                  strokeWidth="1.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </Svg>
              <Text style={styles.metaText}>
                {task.assigned_to.first_name}
              </Text>
            </View>
          )}
        </View>
      </Card.Content>
    </Card>
  );

  const renderStatusSection = (status: keyof TasksByStatus) => {
    const statusTasks = tasksByStatus[status];
    if (statusTasks.length === 0) return null;

    return (
      <View key={status} style={styles.statusSection}>
        <View style={styles.statusHeader}>
          <Text style={styles.statusTitle}>{getStatusTitle(status)}</Text>
          <Badge variant="secondary" style={styles.statusCount}>
            {statusTasks.length}
          </Badge>
        </View>
        
        {statusTasks.map(task => renderTaskItem(task, status))}
      </View>
    );
  };

  const TaskDetailModal = () => (
    <Modal
      visible={isModalVisible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={() => setIsModalVisible(false)}
    >
      <SafeAreaView style={styles.modalContainer}>
        <View style={styles.modalHeader}>
          <Text style={styles.modalTitle}>Детали задачи</Text>
          <TouchableOpacity
            style={styles.closeButton}
            onPress={() => setIsModalVisible(false)}
          >
            <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
              <Path
                d="M18 6L6 18"
                stroke="#64748B"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M6 6L18 18"
                stroke="#64748B"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </TouchableOpacity>
        </View>

        {selectedTask && (
          <ScrollView style={styles.modalContent}>
            <Card>
              <Card.Header>
                <Card.Title>{selectedTask.title}</Card.Title>
                <Badge variant={getStatusBadgeVariant(selectedTask.status)} style={styles.modalBadge}>
                  {getStatusTitle(selectedTask.status)}
                </Badge>
              </Card.Header>
              
              <Card.Content>
                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Описание</Text>
                  <Text style={styles.modalSectionText}>{selectedTask.description}</Text>
                </View>

                <View style={styles.modalSection}>
                  <Text style={styles.modalSectionTitle}>Срок выполнения</Text>
                  <Text style={styles.modalSectionText}>
                    {new Date(selectedTask.due_date).toLocaleDateString('ru-RU')}
                  </Text>
                </View>

                {selectedTask.assigned_to && (
                  <View style={styles.modalSection}>
                    <Text style={styles.modalSectionTitle}>Назначено</Text>
                    <Text style={styles.modalSectionText}>
                      {selectedTask.assigned_to.first_name} {selectedTask.assigned_to.last_name}
                    </Text>
                  </View>
                )}

                {user?.role !== 'DRIVER' || selectedTask.assigned_to?.id === user?.id ? (
                  <View style={styles.actionButtons}>
                    <Text style={styles.actionTitle}>Изменить статус</Text>
                    
                    {selectedTask.status !== 'IN_PROGRESS' && selectedTask.status !== 'COMPLETED' && (
                      <Button
                        variant="secondary"
                        style={styles.actionButton}
                        onPress={() => updateTaskStatus(selectedTask.id, 'IN_PROGRESS')}
                      >
                        Взять в работу
                      </Button>
                    )}

                    {selectedTask.status === 'IN_PROGRESS' && (
                      <Button
                        variant="default"
                        style={styles.actionButton}
                        onPress={() => updateTaskStatus(selectedTask.id, 'COMPLETED')}
                      >
                        Завершить
                      </Button>
                    )}
                  </View>
                ) : (
                  <View style={styles.noPermissionContainer}>
                    <Text style={styles.noPermissionText}>
                      У вас нет прав для изменения этой задачи
                    </Text>
                  </View>
                )}
              </Card.Content>
            </Card>
          </ScrollView>
        )}
      </SafeAreaView>
    </Modal>
  );

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Загрузка задач...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Задачи</Text>
        <View style={styles.headerActions}>
          <TouchableOpacity style={styles.headerButton}>
            <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
              <Path
                d="M18 8C18 6.4087 17.3679 4.88258 16.2426 3.75736C15.1174 2.63214 13.5913 2 12 2C10.4087 2 8.88258 2.63214 7.75736 3.75736C6.63214 4.88258 6 6.4087 6 8C6 15 3 17 3 17H21C21 17 18 15 18 8Z"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M13.73 21C13.5542 21.3031 13.3019 21.5547 12.9982 21.7295C12.6946 21.9044 12.3504 21.9965 12 21.9965C11.6496 21.9965 11.3054 21.9044 11.0018 21.7295C10.6982 21.5547 10.4458 21.3031 10.27 21"
                stroke="#64748B"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </TouchableOpacity>
          <TouchableOpacity style={styles.profileButton}>
            <Svg width={20} height={20} viewBox="0 0 24 24" fill="none">
              <Path
                d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21"
                stroke="#F8FAFC"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <Path
                d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z"
                stroke="#F8FAFC"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </Svg>
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        showsVerticalScrollIndicator={false}
      >
        {['NEW', 'IN_PROGRESS', 'COMPLETED'].map(status => 
          renderStatusSection(status as keyof TasksByStatus)
        )}
      </ScrollView>

      <View style={styles.createButtonContainer}>
        <Button size="lg" style={styles.createButton}>
          Создать задачу
        </Button>
      </View>

      <TaskDetailModal />
    </SafeAreaView>
  );
};

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
    paddingVertical: 16,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E2E8F0',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: '#020817',
    letterSpacing: -0.025,
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  headerButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#F1F5F9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#64748B',
    justifyContent: 'center',
    alignItems: 'center',
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 24,
  },
  statusSection: {
    marginTop: 24,
  },
  statusHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
    gap: 8,
  },
  statusTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#020817',
    letterSpacing: -0.025,
  },
  statusCount: {
    minWidth: 24,
  },
  taskCard: {
    marginBottom: 12,
  },
  taskContent: {
    paddingHorizontal: 20,
    paddingVertical: 16,
  },
  taskHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
    gap: 12,
  },
  taskTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#020817',
    letterSpacing: -0.025,
    flex: 1,
  },
  taskDescription: {
    fontSize: 14,
    color: '#64748B',
    lineHeight: 20,
    marginBottom: 12,
  },
  taskFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 16,
  },
  taskMeta: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  metaIcon: {
    marginRight: 2,
  },
  metaText: {
    fontSize: 12,
    color: '#64748B',
    fontWeight: '500',
  },
  createButtonContainer: {
    paddingHorizontal: 24,
    paddingBottom: 24,
    paddingTop: 16,
    backgroundColor: '#F8FAFC',
  },
  createButton: {
    width: '100%',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F8FAFC',
  },
  loadingText: {
    fontSize: 16,
    color: '#64748B',
    fontWeight: '500',
  },
  
  // Modal styles
  modalContainer: {
    flex: 1,
    backgroundColor: '#F8FAFC',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingVertical: 16,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E2E8F0',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#020817',
    letterSpacing: -0.025,
  },
  closeButton: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#F1F5F9',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    flex: 1,
    padding: 24,
  },
  modalBadge: {
    marginTop: 8,
    alignSelf: 'flex-start',
  },
  modalSection: {
    marginBottom: 20,
  },
  modalSectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#020817',
    marginBottom: 4,
    letterSpacing: -0.025,
  },
  modalSectionText: {
    fontSize: 14,
    color: '#64748B',
    lineHeight: 20,
  },
  actionButtons: {
    marginTop: 24,
    gap: 12,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#020817',
    marginBottom: 12,
    letterSpacing: -0.025,
  },
  actionButton: {
    width: '100%',
  },
  noPermissionContainer: {
    marginTop: 24,
    padding: 16,
    backgroundColor: '#FEF3C7',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#F59E0B',
  },
  noPermissionText: {
    fontSize: 14,
    color: '#92400E',
    textAlign: 'center',
    fontWeight: '500',
  },
});

export default TasksScreen; 