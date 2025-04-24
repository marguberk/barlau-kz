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
  });

  // Определяем, запущено ли приложение из установленного PWA
  if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    console.log('Приложение запущено в режиме standalone');
    // Здесь можно добавить логику для установленного приложения
    document.body.classList.add('pwa-installed');
  }
}); 