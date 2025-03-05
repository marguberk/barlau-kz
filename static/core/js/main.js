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
});
