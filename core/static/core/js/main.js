console.log('main.js подключён!');
// Всплывающая карточка уведомления
function showToastNotification(title, message, link = null, type = null) {
    // Воспроизвести звук уведомления (mp3 -> wav)
    try {
        let audio = new Audio('/static/core/sounds/notification.mp3');
        audio.play().catch(() => {
            let audioWav = new Audio('/static/core/sounds/notification.wav');
            audioWav.play();
        });
    } catch (e) {}
    // Если уже есть тост — удаляем
    const oldToast = document.getElementById('toast-notification');
    if (oldToast) oldToast.remove();

    // Создаём контейнер
    const toast = document.createElement('div');
    toast.id = 'toast-notification';
    toast.className = 'fixed z-[9999] right-6 top-[4.5rem] bg-white border border-blue-500 shadow-xl rounded-xl px-5 py-4 flex items-start gap-3 animate-fade-in-up';
    toast.style.minWidth = '320px';
    toast.style.maxWidth = '90vw';
    toast.style.transition = 'opacity 0.4s, transform 0.4s';
    toast.style.pointerEvents = 'auto';
    toast.style.boxSizing = 'border-box';
    toast.style.overflow = 'hidden';

    // --- Цвет и иконка для типа ---
    let iconHtml = '<i class="fa fa-bell text-blue-500 text-2xl"></i>';
    let iconBg = '#e0e7ff';
    let borderColor = '#3b82f6';
    if (type === 'DOCUMENT' || title.toLowerCase().includes('документ')) {
        iconHtml = '<i class="fa fa-exclamation-triangle text-red-500 text-2xl"></i>';
        iconBg = '#fef2f2';
        borderColor = '#f87171';
        toast.style.borderColor = borderColor;
    }

    // Иконка
    const icon = document.createElement('span');
    icon.innerHTML = iconHtml;
    icon.style.background = iconBg;
    icon.style.borderRadius = '50%';
    icon.style.width = '2.5rem';
    icon.style.height = '2.5rem';
    icon.style.display = 'flex';
    icon.style.alignItems = 'center';
    icon.style.justifyContent = 'center';
    toast.appendChild(icon);

    // Контент
    const content = document.createElement('div');
    content.className = 'flex flex-col';
    content.innerHTML = `<div class='font-semibold text-blue-600 mb-1'>${title}</div><div class='text-gray-700 mb-1'>${message}</div>`;
    toast.appendChild(content);

    // Кнопка закрытия
    const closeBtn = document.createElement('button');
    closeBtn.innerHTML = '<i class="fa fa-times text-gray-400 text-lg"></i>';
    closeBtn.className = 'absolute top-2 right-3';
    closeBtn.style.background = 'none';
    closeBtn.style.border = 'none';
    closeBtn.style.cursor = 'pointer';
    closeBtn.onclick = () => {
        toast.style.transform = 'translateX(120%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 400);
    };
    toast.appendChild(closeBtn);

    // Прогресс-бар
    const progress = document.createElement('div');
    progress.style.position = 'absolute';
    progress.style.left = '0.75rem';
    progress.style.top = '0.5rem';
    progress.style.width = 'calc(100% - 2.5rem)';
    progress.style.height = '5px';
    progress.style.background = '#e5e7eb';
    progress.style.borderRadius = '3px';
    progress.style.overflow = 'hidden';
    progress.style.zIndex = '1';
    // Цвет прогресса по типу
    let progColor = '#3b82f6';
    if (type === 'DOCUMENT' || title.toLowerCase().includes('документ')) progColor = '#f87171';
    const progBar = document.createElement('div');
    progBar.style.height = '100%';
    progBar.style.width = '100%';
    progBar.style.background = progColor;
    progBar.style.borderRadius = '3px';
    progBar.style.transition = 'width 0.4s linear';
    progress.appendChild(progBar);
    toast.appendChild(progress);
    toast.style.position = 'fixed';
    toast.style.top = '4.5rem';
    toast.style.right = '1.5rem';
    toast.style.left = 'auto';

    // Добавляем в body
    document.body.appendChild(toast);

    // Анимация прогресса и исчезновения
    setTimeout(() => {
        progBar.style.width = '0%';
    }, 50);
    setTimeout(() => {
        toast.style.transform = 'translateX(120%)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 400);
    }, 4000);
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
                    showToastNotification(notif.title, notif.message, notif.link, notif.type);
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
            badge.style.fontSize = '0.75rem';
            badge.style.fontWeight = 600;
            badge.style.color = '#fff';
            badge.style.padding = '0 0.38em';
            badge.style.justifyContent = 'center';
            badge.style.alignItems = 'center';
        } else {
            badge.textContent = '';
            badge.style.opacity = '0';
            badge.style.display = 'none';
        }
    } catch (e) { console.log('[DEBUG] badge error', e); }
}
window.updateGlobalNotifBadge = updateGlobalNotifBadge;
window.addEventListener('DOMContentLoaded', () => {
    updateGlobalNotifBadge();
    // showToastNotification('Тест', 'Проверка звука'); // убрано
});
setInterval(updateGlobalNotifBadge, 15000); 