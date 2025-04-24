/**
 * offline.js - Управление офлайн-режимом для BARLAU.KZ
 * Этот скрипт обеспечивает обработку офлайн-состояния приложения и управление
 * сохранением данных при отсутствии подключения к интернету
 */

// Инициализация переменных для отслеживания статуса подключения
let isOnline = navigator.onLine;
let offlineMode = false;
let pendingSyncs = 0;
let offlineIndicator = null;
let syncButton = null;

// Инициализация офлайн-функциональности
document.addEventListener('DOMContentLoaded', () => {
  // Создание индикатора офлайн-режима
  createOfflineIndicator();
  
  // Создание кнопки синхронизации
  createSyncButton();
  
  // Установка начального состояния
  updateOfflineStatus();
  
  // Обработчики событий подключения/отключения
  window.addEventListener('online', handleConnectionChange);
  window.addEventListener('offline', handleConnectionChange);
  
  // Регистрация обработчика сообщений от service worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', handleServiceWorkerMessage);
  }
  
  // Инициализация IndexedDB для хранения данных
  initDatabase();
});

// Создание индикатора офлайн-режима
function createOfflineIndicator() {
  offlineIndicator = document.createElement('div');
  offlineIndicator.id = 'offline-indicator';
  offlineIndicator.className = 'offline-indicator hidden';
  offlineIndicator.innerHTML = `
    <div class="offline-indicator-content">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="1" y1="1" x2="23" y2="23"></line>
        <path d="M16.72 11.06A10.94 10.94 0 0 1 19 12.55"></path>
        <path d="M5 12.55a10.94 10.94 0 0 1 5.17-2.39"></path>
        <path d="M10.71 5.05A16 16 0 0 1 22.58 9"></path>
        <path d="M1.42 9a15.91 15.91 0 0 1 4.7-2.88"></path>
        <path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path>
        <line x1="12" y1="20" x2="12.01" y2="20"></line>
      </svg>
      <span>Офлайн-режим</span>
    </div>
  `;
  
  // Добавление стилей для индикатора
  const style = document.createElement('style');
  style.textContent = `
    .offline-indicator {
      position: fixed;
      bottom: 20px;
      left: 20px;
      background-color: #f44336;
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      z-index: 1000;
      transition: opacity 0.3s, transform 0.3s;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .offline-indicator.hidden {
      opacity: 0;
      transform: translateY(20px);
      pointer-events: none;
    }
    
    .offline-indicator-content {
      display: flex;
      align-items: center;
    }
    
    .offline-indicator svg {
      margin-right: 8px;
    }
    
    @media (max-width: 768px) {
      .offline-indicator {
        bottom: 70px; /* Отступ для мобильных устройств, чтобы не перекрывать нижнюю навигацию */
      }
    }
  `;
  
  document.head.appendChild(style);
  document.body.appendChild(offlineIndicator);
}

// Создание кнопки синхронизации
function createSyncButton() {
  syncButton = document.createElement('button');
  syncButton.id = 'sync-button';
  syncButton.className = 'sync-button hidden';
  syncButton.innerHTML = `
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="1 4 1 10 7 10"></polyline>
      <polyline points="23 20 23 14 17 14"></polyline>
      <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"></path>
    </svg>
    <span>Синхронизировать</span>
    <span class="sync-badge">0</span>
  `;
  
  // Добавление стилей для кнопки синхронизации
  const style = document.createElement('style');
  style.textContent = `
    .sync-button {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background-color: #2196F3;
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      display: flex;
      align-items: center;
      z-index: 1000;
      transition: opacity 0.3s, transform 0.3s;
      border: none;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .sync-button:hover {
      background-color: #1976D2;
    }
    
    .sync-button.hidden {
      opacity: 0;
      transform: translateY(20px);
      pointer-events: none;
    }
    
    .sync-button svg {
      margin-right: 8px;
    }
    
    .sync-badge {
      background-color: #FF5722;
      border-radius: 50%;
      min-width: 20px;
      height: 20px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-left: 8px;
      font-size: 12px;
    }
    
    @media (max-width: 768px) {
      .sync-button {
        bottom: 70px; /* Отступ для мобильных устройств */
        right: 16px;
      }
    }
  `;
  
  document.head.appendChild(style);
  document.body.appendChild(syncButton);
  
  // Обработчик нажатия кнопки синхронизации
  syncButton.addEventListener('click', triggerSync);
}

// Обновление статуса офлайн-режима
function updateOfflineStatus() {
  isOnline = navigator.onLine;
  
  if (!isOnline) {
    offlineMode = true;
    showOfflineIndicator();
    maybeShowInstallPrompt();
  } else if (offlineMode) {
    hideOfflineIndicator();
    
    // Если были в офлайн-режиме и появилось подключение,
    // пытаемся синхронизировать сохраненные запросы
    if (pendingSyncs > 0) {
      showSyncButton();
    } else {
      hideSyncButton();
    }
  }
}

// Обработка изменения статуса подключения
function handleConnectionChange(event) {
  if (event.type === 'online') {
    console.log('Соединение восстановлено');
    if (offlineMode) {
      offlineMode = false;
      
      // Показываем уведомление о восстановлении соединения
      showToast('Соединение восстановлено', 'success');
      
      // Скрываем индикатор офлайн-режима
      hideOfflineIndicator();
      
      // Если есть ожидающие синхронизации данные, показываем кнопку синхронизации
      if (pendingSyncs > 0) {
        showSyncButton();
      }
    }
  } else if (event.type === 'offline') {
    console.log('Соединение потеряно');
    offlineMode = true;
    
    // Показываем уведомление о потере соединения
    showToast('Отсутствует подключение к интернету. Приложение работает в офлайн-режиме.', 'warning');
    
    // Показываем индикатор офлайн-режима
    showOfflineIndicator();
    
    // Проверяем, можно ли предложить установку приложения
    maybeShowInstallPrompt();
  }
}

// Обработка сообщений от service worker
function handleServiceWorkerMessage(event) {
  if (event.data && event.data.type === 'sync-complete') {
    if (event.data.success) {
      pendingSyncs = 0;
      updateSyncBadge();
      
      // Если нет больше данных для синхронизации, скрываем кнопку
      if (pendingSyncs === 0) {
        hideSyncButton();
      }
      
      showToast('Синхронизация завершена успешно', 'success');
    } else {
      showToast('Ошибка при синхронизации данных', 'error');
    }
  } else if (event.data && event.data.type === 'pending-sync') {
    pendingSyncs = event.data.count || 0;
    updateSyncBadge();
    
    // Показываем кнопку синхронизации, если есть что синхронизировать
    if (pendingSyncs > 0 && isOnline) {
      showSyncButton();
    }
  }
}

// Запуск синхронизации
function triggerSync() {
  if ('serviceWorker' in navigator && 'SyncManager' in window && navigator.onLine) {
    navigator.serviceWorker.ready
      .then(registration => {
        // Добавляем анимацию для кнопки синхронизации
        syncButton.classList.add('syncing');
        
        // Запускаем синхронизацию
        return registration.sync.register('sync-data')
          .then(() => {
            console.log('Синхронизация запущена');
            showToast('Синхронизация данных...', 'info');
          })
          .catch(error => {
            console.error('Ошибка при запуске синхронизации:', error);
            showToast('Не удалось запустить синхронизацию', 'error');
            
            // Убираем анимацию
            syncButton.classList.remove('syncing');
          });
      });
  } else {
    showToast('Синхронизация недоступна в офлайн-режиме', 'warning');
  }
}

// Обновление счетчика ожидающих синхронизаций
function updateSyncBadge() {
  const badge = syncButton.querySelector('.sync-badge');
  if (badge) {
    badge.textContent = pendingSyncs;
    badge.style.display = pendingSyncs > 0 ? 'flex' : 'none';
  }
}

// Показать индикатор офлайн-режима
function showOfflineIndicator() {
  if (offlineIndicator) {
    offlineIndicator.classList.remove('hidden');
  }
}

// Скрыть индикатор офлайн-режима
function hideOfflineIndicator() {
  if (offlineIndicator) {
    offlineIndicator.classList.add('hidden');
  }
}

// Показать кнопку синхронизации
function showSyncButton() {
  if (syncButton) {
    syncButton.classList.remove('hidden');
    updateSyncBadge();
  }
}

// Скрыть кнопку синхронизации
function hideSyncButton() {
  if (syncButton) {
    syncButton.classList.add('hidden');
  }
}

// Показать всплывающее уведомление
function showToast(message, type = 'info') {
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      text: message,
      icon: type,
      toast: true,
      position: 'bottom-end',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true
    });
  } else {
    // Создаем простое уведомление, если SweetAlert не доступен
    const toast = document.createElement('div');
    toast.className = `simple-toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // Показываем уведомление
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);
    
    // Скрываем и удаляем через 3 секунды
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 3000);
    
    // Стили для простого уведомления
    if (!document.querySelector('#simple-toast-styles')) {
      const style = document.createElement('style');
      style.id = 'simple-toast-styles';
      style.textContent = `
        .simple-toast {
          position: fixed;
          bottom: 20px;
          right: 20px;
          padding: 10px 20px;
          border-radius: 4px;
          color: white;
          max-width: 300px;
          z-index: 10000;
          opacity: 0;
          transform: translateY(20px);
          transition: opacity 0.3s, transform 0.3s;
          box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        
        .simple-toast.show {
          opacity: 1;
          transform: translateY(0);
        }
        
        .simple-toast.info {
          background-color: #2196F3;
        }
        
        .simple-toast.success {
          background-color: #4CAF50;
        }
        
        .simple-toast.warning {
          background-color: #FF9800;
        }
        
        .simple-toast.error {
          background-color: #F44336;
        }
        
        @media (max-width: 768px) {
          .simple-toast {
            bottom: 70px;
          }
        }
      `;
      document.head.appendChild(style);
    }
  }
}

// Возможно предложить установку PWA при потере соединения
function maybeShowInstallPrompt() {
  // Проверяем, запущено ли приложение как PWA
  if (!navigator.standalone && !window.matchMedia('(display-mode: standalone)').matches) {
    // Если приложение не установлено, предлагаем установить для офлайн-работы
    if (window.deferredPrompt) {
      showInstallPrompt();
    }
  }
}

// Показать предложение установить приложение
function showInstallPrompt() {
  if (typeof Swal !== 'undefined') {
    Swal.fire({
      title: 'Установить приложение',
      text: 'Установите приложение для работы в офлайн-режиме',
      icon: 'info',
      showCancelButton: true,
      confirmButtonText: 'Установить',
      cancelButtonText: 'Не сейчас'
    }).then((result) => {
      if (result.isConfirmed) {
        // Показываем запрос на установку
        window.deferredPrompt.prompt();
        
        // Ожидаем ответа пользователя
        window.deferredPrompt.userChoice.then((choiceResult) => {
          if (choiceResult.outcome === 'accepted') {
            console.log('Пользователь установил приложение');
          } else {
            console.log('Пользователь отклонил установку');
          }
          // Сбрасываем запрос на установку
          window.deferredPrompt = null;
        });
      }
    });
  }
}

// Инициализация IndexedDB для хранения офлайн-данных
function initDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('barlau-offline-db', 1);
    
    request.onupgradeneeded = event => {
      const db = event.target.result;
      
      // Создаем хранилища для основных типов данных, которые могут редактироваться офлайн
      if (!db.objectStoreNames.contains('tasks')) {
        db.createObjectStore('tasks', { keyPath: 'id' });
      }
      
      if (!db.objectStoreNames.contains('trips')) {
        db.createObjectStore('trips', { keyPath: 'id' });
      }
      
      if (!db.objectStoreNames.contains('forms')) {
        const formsStore = db.createObjectStore('forms', { keyPath: 'id', autoIncrement: true });
        formsStore.createIndex('formType', 'formType', { unique: false });
        formsStore.createIndex('timestamp', 'timestamp', { unique: false });
      }
    };
    
    request.onsuccess = event => {
      console.log('База данных офлайн-режима успешно инициализирована');
      resolve(event.target.result);
    };
    
    request.onerror = event => {
      console.error('Ошибка при инициализации базы данных:', event.target.error);
      reject(event.target.error);
    };
  });
}

// Сохранение формы в IndexedDB для последующей синхронизации
function saveFormForSync(formType, formData) {
  return new Promise((resolve, reject) => {
    initDatabase().then(db => {
      const transaction = db.transaction(['forms'], 'readwrite');
      const store = transaction.objectStore('forms');
      
      const record = {
        formType,
        formData,
        timestamp: Date.now(),
        status: 'pending'
      };
      
      const request = store.add(record);
      
      request.onsuccess = event => {
        console.log('Форма сохранена для последующей синхронизации', event.target.result);
        pendingSyncs++;
        updateSyncBadge();
        
        if (isOnline) {
          showSyncButton();
        }
        
        resolve(event.target.result);
      };
      
      request.onerror = event => {
        console.error('Ошибка при сохранении формы:', event.target.error);
        reject(event.target.error);
      };
    }).catch(reject);
  });
}

// Экспорт API для использования в других скриптах
window.offlineAPI = {
  isOffline: () => offlineMode,
  saveFormForSync,
  triggerSync,
  showToast
}; 