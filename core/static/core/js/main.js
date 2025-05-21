console.log('main.js подключён!');
// Всплывающая карточка уведомления
function showToastNotification(title, message, link = null) {
    // Воспроизвести звук уведомления (mp3 -> wav)
    try {
        let audio = new Audio('/static/core/sounds/notification.mp3');
        audio.play().then(()=>console.log('[DEBUG] mp3 played')).catch((err) => {
            console.log('[DEBUG] mp3 error', err);
            let audioWav = new Audio('/static/core/sounds/notification.wav');
            audioWav.play().then(()=>console.log('[DEBUG] wav played')).catch((err)=>console.log('[DEBUG] wav error', err));
        });
    } catch (e) { console.log('[DEBUG] audio error', e); }
    // Если уже есть тост — удаляем
    const oldToast = document.getElementById('toast-notification');
    if (oldToast) oldToast.remove();

    // Создаём контейнер
    const toast = document.createElement('div');
    toast.id = 'toast-notification';
    toast.className = 'fixed z-[9999] right-4 top-6 bg-white border border-blue-500 shadow-xl rounded-xl px-5 py-4 flex items-start gap-3 animate-fade-in-down';
    toast.style.minWidth = '320px';
    toast.style.maxWidth = '90vw';
    toast.style.transition = 'opacity 0.4s, transform 0.4s';

    // Полоса-таймер
    const timerBar = document.createElement('div');
    timerBar.className = 'absolute left-0 top-0 h-1 bg-blue-500 rounded-t-xl';
    timerBar.style.width = '100%';
    timerBar.style.transition = 'width 5s linear';
    toast.appendChild(timerBar);
    setTimeout(() => { timerBar.style.width = '0%'; }, 10);

    // Иконка
    const icon = document.createElement('span');
    icon.innerHTML = `<i class="fa fa-bell text-blue-500 text-2xl"></i>`;
    toast.appendChild(icon);

    // Контент
    const content = document.createElement('div');
    content.innerHTML = `<div class="font-semibold text-base text-blue-700">${title}</div><div class="text-gray-700 text-sm mt-1">${message}</div>`;
    if (link) {
        content.innerHTML += `<a href="${link}" class="text-blue-600 hover:underline text-xs mt-2 inline-block">Подробнее</a>`;
    }
    toast.appendChild(content);

    // Кнопка закрытия
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '&times;';
    closeBtn.className = 'ml-4 text-gray-400 hover:text-gray-700 text-xl font-bold focus:outline-none';
    closeBtn.onclick = () => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-40px)';
        setTimeout(() => toast.remove(), 400);
    };
    toast.appendChild(closeBtn);

    // Анимация появления
    toast.animate([
        { opacity: 0, transform: 'translateY(-40px)' },
        { opacity: 1, transform: 'translateY(0)' }
    ], {
        duration: 400,
        fill: 'forwards'
    });

    toast.style.position = 'fixed';
    toast.style.right = '1rem';
    toast.style.top = '1.5rem';
    toast.style.left = '';
    toast.style.bottom = '';
    toast.style.zIndex = 9999;
    toast.style.boxShadow = '0 8px 32px rgba(37,99,235,0.15)';
    toast.style.overflow = 'visible';
    toast.style.paddingTop = '1.5rem';

    document.body.appendChild(toast);

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-40px)';
            setTimeout(() => toast.remove(), 400);
        }
    }, 5000);
}

// Пример использования (раскомментируй для теста)
// showToastNotification('Новое уведомление', 'Это пример всплывающей карточки уведомления!');

// Для интеграции: вызывай showToastNotification(title, message, link) при получении нового уведомления через WebSocket или polling 

// --- Polling для новых уведомлений ---
let lastNotifId = null;

async function checkNewNotifications() {
    try {
        const response = await fetch('/api/notifications/?unread=true&page_size=1');
        if (!response.ok) return;
        const data = await response.json();
        if (data.results && data.results.length > 0) {
            const notif = data.results[0];
            if (notif.id !== lastNotifId) {
                // Показываем toast только если это новое уведомление
                if (lastNotifId !== null) {
                    showToastNotification(notif.title, notif.message, notif.link);
                }
                lastNotifId = notif.id;
            }
        }
    } catch (e) {
        // ignore
    }
}

// Получаем id последнего уведомления при загрузке
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/notifications/?unread=true&page_size=1');
        if (!response.ok) return;
        const data = await response.json();
        if (data.results && data.results.length > 0) {
            lastNotifId = data.results[0].id;
        }
    } catch (e) {}
    setInterval(checkNewNotifications, 10000); // каждые 10 секунд
});

// --- Обновление бейджа уведомлений на всех страницах ---
async function updateGlobalNotifBadge() {
    const badge = document.getElementById('notif-badge');
    if (!badge) return;
    try {
        const response = await fetch('/api/notifications/unread_count/', { credentials: 'same-origin' });
        if (!response.ok) return;
        const data = await response.json();
        console.log('[DEBUG] unread_count:', data.count);
        if (data.count && data.count > 0) {
            badge.textContent = data.count > 99 ? '99+' : data.count;
            badge.style.opacity = '1';
            badge.style.display = 'flex';
            badge.style.width = badge.style.height = '1.4rem';
            badge.style.fontSize = '0.85rem';
            badge.style.color = '#fff';
            badge.style.padding = '0 0.3em';
            badge.style.justifyContent = 'center';
            badge.style.alignItems = 'center';
        } else {
            badge.textContent = '';
            badge.style.opacity = '0';
            badge.style.display = 'none';
        }
    } catch (e) { console.log('[DEBUG] badge error', e); }
}
window.addEventListener('DOMContentLoaded', () => {
    updateGlobalNotifBadge();
    // showToastNotification('Тест', 'Проверка звука'); // убрано
});
setInterval(updateGlobalNotifBadge, 15000); 