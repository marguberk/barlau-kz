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
    
    // Добавляем класс для установленного приложения
    document.body.classList.add('pwa-installed');
    
    // Переключаемся на мобильные иконки сразу после установки
    switchToMobileIcons();
  });

  // Определяем, запущено ли приложение из установленного PWA
  if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    console.log('Приложение запущено в режиме standalone');
    
    // Добавляем класс для установленного приложения
    document.body.classList.add('pwa-installed');
    
    // Переключаемся на мобильные иконки для установленных приложений
    switchToMobileIcons();
  }
  
  // Определяем, является ли устройство мобильным
  if (isMobileDevice()) {
    console.log('Обнаружено мобильное устройство');
    
    // Добавляем класс для мобильных устройств
    document.body.classList.add('mobile-device');
    
    // Переключаемся на мобильные иконки для мобильных устройств
    switchToMobileIcons();
  }
  
  // Функция для определения мобильного устройства
  function isMobileDevice() {
    return (
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || 
      (window.innerWidth <= 768)
    );
  }
  
  // Функция для переключения на мобильные иконки
  function switchToMobileIcons() {
    // Скрываем десктопные иконки и показываем мобильные
    document.querySelectorAll('.desktop-icon').forEach(function(icon) {
      icon.style.display = 'none';
    });
    
    document.querySelectorAll('.mobile-icon').forEach(function(icon) {
      icon.style.display = 'block';
      // Увеличиваем размер иконок для лучшей видимости на мобильных устройствах
      icon.style.width = '32px';
      icon.style.height = '32px';
    });
    
    // Обрабатываем стиль для активных элементов меню с мобильными иконками
    document.querySelectorAll('.text-blue-600 .mobile-icon').forEach(function(icon) {
      icon.style.filter = 'invert(37%) sepia(74%) saturate(1775%) hue-rotate(211deg) brightness(95%) contrast(98%)';
    });
  }
  
  // Слушаем изменения ориентации устройства
  window.addEventListener('orientationchange', function() {
    if (isMobileDevice() || document.body.classList.contains('pwa-installed')) {
      // Убеждаемся, что иконки остаются правильными после смены ориентации
      setTimeout(switchToMobileIcons, 300);
    }
  });
}); 