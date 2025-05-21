// Всплывающая карточка уведомления
function showToastNotification(title, message, link = null) {
    // Если уже есть тост — удаляем
    const oldToast = document.getElementById('toast-notification');
    if (oldToast) oldToast.remove();

    // Создаём контейнер
    const toast = document.createElement('div');
    toast.id = 'toast-notification';
    toast.className = 'fixed z-[9999] right-4 bottom-6 bg-white border border-blue-500 shadow-xl rounded-xl px-5 py-4 flex items-start gap-3 animate-fade-in-up';
    toast.style.minWidth = '320px';
    toast.style.maxWidth = '90vw';
    toast.style.transition = 'opacity 0.4s, transform 0.4s';

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
        toast.style.transform = 'translateY(40px)';
        setTimeout(() => toast.remove(), 400);
    };
    toast.appendChild(closeBtn);

    // Анимация появления
    toast.animate([
        { opacity: 0, transform: 'translateY(40px)' },
        { opacity: 1, transform: 'translateY(0)' }
    ], {
        duration: 400,
        fill: 'forwards'
    });

    document.body.appendChild(toast);

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        if (toast.parentNode) {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(40px)';
            setTimeout(() => toast.remove(), 400);
        }
    }, 5000);
}

// Пример использования (раскомментируй для теста)
// showToastNotification('Новое уведомление', 'Это пример всплывающей карточки уведомления!');

// Для интеграции: вызывай showToastNotification(title, message, link) при получении нового уведомления через WebSocket или polling 