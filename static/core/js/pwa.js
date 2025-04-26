// Скрипт для регистрации Service Worker и инициализации PWA
document.addEventListener('DOMContentLoaded', function() {
  // Проверяем поддержку Service Worker
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
      navigator.serviceWorker.register('/static/core/js/service-worker.js')
        .then(function(registration) {
          console.log('ServiceWorker успешно зарегистрирован со scope: ', registration.scope);
        })
        .catch(function(error) {
          console.log('Ошибка регистрации ServiceWorker: ', error);
        });
    });
  }

  // Определяем тип устройства для лучшей адаптации
  const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
  const isTablet = /iPad|Android/.test(navigator.userAgent) && !/Mobile/.test(navigator.userAgent) || (window.innerWidth >= 768 && window.innerWidth <= 1100);
  
  // Добавляем соответствующие классы к body
  if (isMobile) {
    document.body.classList.add('mobile-device');
  }
  if (isTablet) {
    document.body.classList.add('tablet-device');
  }
  
  // Настраиваем адаптированное отображение SVG иконок
  if (isMobile || isTablet) {
    showMobileIcons();
  }

  // Обработка установки PWA
  let deferredPrompt;
  const installButton = document.getElementById('install-button');
  
  // Скрываем кнопку установки по умолчанию
  if (installButton) {
    installButton.style.display = 'none';
  }

  // Обрабатываем событие 'beforeinstallprompt'
  window.addEventListener('beforeinstallprompt', (e) => {
    // Предотвращаем автоматический показ диалога установки
    e.preventDefault();
    // Сохраняем событие для использования позже
    deferredPrompt = e;
    
    // Показываем кнопку установки если она существует
    if (installButton) {
      installButton.style.display = 'block';
      
      // Для мобильных устройств делаем кнопку более заметной
      if (isMobile) {
        installButton.classList.add('animate-pulse-slow');
      }
      
      // Обрабатываем клик по кнопке установки
      installButton.addEventListener('click', async () => {
        // Скрываем кнопку после нажатия
        installButton.style.display = 'none';
        
        // Показываем диалог установки
        deferredPrompt.prompt();
        
        // Ожидаем выбор пользователя
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`Результат выбора: ${outcome}`);
        
        // Очищаем сохраненное событие
        deferredPrompt = null;
      });
    }
  });

  // Обрабатываем событие успешной установки
  window.addEventListener('appinstalled', (evt) => {
    console.log('Приложение установлено');
    // Очищаем сохраненное событие
    deferredPrompt = null;
    
    // Отображаем благодарственное сообщение
    if (typeof showAlert === 'function') {
      showAlert('Приложение установлено', 'Спасибо за установку BARLAU.KZ на ваше устройство!', 'success');
    }
  });

  // Определяем, запущено ли приложение из установленного PWA
  if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    console.log('Приложение запущено в режиме standalone');
    // Добавляем класс для установленного приложения
    document.body.classList.add('pwa-installed');
    
    // Адаптируем интерфейс для запуска из PWA
    optimizeForStandaloneMode();
  }
  
  // Отслеживаем изменение режима отображения
  window.matchMedia('(display-mode: standalone)').addEventListener('change', (evt) => {
    if (evt.matches) {
      document.body.classList.add('pwa-installed');
      optimizeForStandaloneMode();
    } else {
      document.body.classList.remove('pwa-installed');
    }
  });
});

// Функция для отображения мобильных иконок
function showMobileIcons() {
  // Скрываем десктопные иконки и показываем мобильные
  document.querySelectorAll('.desktop-icon').forEach(function(icon) {
    icon.style.display = 'none';
  });
  
  document.querySelectorAll('.mobile-icon').forEach(function(icon) {
    icon.style.display = 'block';
    icon.style.width = '32px';
    icon.style.height = '32px';
  });
}

// Функция для оптимизации под standalone режим
function optimizeForStandaloneMode() {
  // Удаляем ненужные элементы для PWA
  const headerLinks = document.querySelectorAll('header a[href]:not([href="/"])');
  headerLinks.forEach(link => {
    // Удаляем внешние ссылки из шапки в режиме приложения
    if (!link.getAttribute('href').startsWith('/')) {
      link.style.display = 'none';
    }
  });
  
  // Увеличиваем тап-зоны для элементов навигации
  document.querySelectorAll('nav a, button').forEach(element => {
    element.style.padding = '12px';
  });
  
  // Обрабатываем офлайн-режим
  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);
  updateOnlineStatus();
}

// Функция для обновления статуса подключения
function updateOnlineStatus() {
  const isOnline = navigator.onLine;
  
  if (!isOnline) {
    // Добавляем индикатор офлайн-режима
    if (!document.getElementById('offline-indicator')) {
      const indicator = document.createElement('div');
      indicator.id = 'offline-indicator';
      indicator.innerHTML = 'Вы работаете в офлайн-режиме';
      indicator.style.cssText = 'position: fixed; bottom: 80px; left: 0; right: 0; background-color: #f97316; color: white; text-align: center; padding: 6px; z-index: 1000; font-size: 14px;';
      document.body.appendChild(indicator);
    }
  } else {
    // Удаляем индикатор, если он есть
    const indicator = document.getElementById('offline-indicator');
    if (indicator) {
      indicator.remove();
    }
    
    // При восстановлении подключения синхронизируем данные
    if ('serviceWorker' in navigator && 'SyncManager' in window) {
      navigator.serviceWorker.ready.then(registration => {
        registration.sync.register('sync-data');
      });
    }
  }
} 