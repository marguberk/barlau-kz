// Основной JavaScript файл для приложения Barlau.kz

document.addEventListener('DOMContentLoaded', function() {
    console.log('Barlau.kz - JavaScript загружен');
    
    // Инициализация Flatpickr для полей с датами
    if (typeof flatpickr !== 'undefined') {
        flatpickr.localize(flatpickr.l10ns.ru);
        const dateInputs = document.querySelectorAll('.date-picker');
        if (dateInputs.length > 0) {
            dateInputs.forEach(input => {
                flatpickr(input, {
                    dateFormat: "Y-m-d",
                    allowInput: true
                });
            });
        }
    }
    
    // Инициализация SweetAlert для сообщений
    window.showAlert = function(title, message, type = 'success') {
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                title: title,
                text: message,
                icon: type,
                confirmButtonText: 'OK',
                confirmButtonColor: '#3b82f6'
            });
        } else {
            alert(title + ': ' + message);
        }
    };

    updateNotifBadgeUniversal();
    setInterval(updateNotifBadgeUniversal, 60000); // Проверять раз в минуту
});

// Универсальный badge для колокольчика уведомлений
async function updateNotifBadgeUniversal() {
    try {
        const badge = document.getElementById('notif-badge');
        if (!badge) return;
        const response = await fetch('/api/notifications/?unread=true', { credentials: 'same-origin' });
        if (!response.ok) {
            badge.classList.add('hidden');
            return;
        }
        const data = await response.json();
        let unread = Array.isArray(data) ? data : (data.results || []);
        if (unread.length > 0) {
            badge.classList.remove('hidden');
        } else {
            badge.classList.add('hidden');
        }
    } catch (e) {
        // В случае ошибки скрываем badge
        const badge = document.getElementById('notif-badge');
        if (badge) badge.classList.add('hidden');
    }
}
