// Тестовое сообщение для проверки загрузки файла
console.log('tasks.js загружен и выполняется!');

// Глобальные переменные
let tasks = [];
let currentTaskId = null;

// Основные элементы DOM
let taskForm, taskModal, modalTitle, loadingIndicator, tasksList, emptyState;
let searchInput, statusFilter, priorityFilter;
let closeButtons, saveTaskBtn;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded: Инициализация страницы задач');
    
    // Инициализация DOM элементов
    initElements();
    
    // Инициализация обработчиков событий
    initEventListeners();
    
    // Загрузка задач
    loadTasks();
});

// Инициализация DOM элементов
function initElements() {
    console.log('Инициализация DOM элементов');
    
    // Основные элементы
    taskModal = document.getElementById('taskModal');
    taskForm = document.getElementById('taskForm');
    modalTitle = document.getElementById('modalTitle');
    loadingIndicator = document.getElementById('loadingIndicator');
    tasksList = document.getElementById('tasksList');
    emptyState = document.getElementById('emptyState');
    
    // Элементы фильтрации
    searchInput = document.getElementById('searchInput');
    statusFilter = document.getElementById('statusFilter');
    priorityFilter = document.getElementById('priorityFilter');
    
    // Кнопки
    saveTaskBtn = document.getElementById('saveTaskBtn');
    closeButtons = document.querySelectorAll('.modal-close');
    
    // Проверка наличия элементов
    if (!taskModal) console.error('Модальное окно не найдено!');
    if (!taskForm) console.error('Форма задачи не найдена!');
    if (!modalTitle) console.error('Заголовок модального окна не найден!');
    if (!loadingIndicator) console.error('Индикатор загрузки не найден!');
    if (!tasksList) console.error('Список задач не найден!');
    if (!emptyState) console.error('Пустое состояние не найдено!');
    if (!searchInput) console.error('Поле поиска не найдено!');
    if (!statusFilter) console.error('Фильтр статуса не найден!');
    if (!priorityFilter) console.error('Фильтр приоритета не найден!');
    if (!saveTaskBtn) console.error('Кнопка сохранения не найдена!');
    
    console.log('DOM элементы инициализированы');
}

// Инициализация обработчиков событий
function initEventListeners() {
    console.log('Настройка обработчиков событий');
    
    // Обработчик кнопки добавления задачи
    const addTaskBtn = document.getElementById('addTaskButton');
    if (addTaskBtn) {
        console.log('Добавление обработчика для кнопки добавления задачи');
        addTaskBtn.addEventListener('click', handleAddTaskClick);
    } else {
        console.error('Кнопка добавления задачи не найдена!');
    }
    
    // Обработчики кнопок закрытия модального окна
    if (closeButtons && closeButtons.length > 0) {
        console.log(`Добавление обработчиков для ${closeButtons.length} кнопок закрытия`);
        closeButtons.forEach(button => {
            button.addEventListener('click', handleCloseModalClick);
        });
    } else {
        console.error('Кнопки закрытия модального окна не найдены!');
    }
    
    // Обработчик формы
    if (taskForm) {
        console.log('Добавление обработчика для формы задачи');
        // отключаем стандартный submit и используем кнопку сохранения
        taskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Предотвращение стандартной отправки формы');
        });
    }
    
    // Обработчик кнопки сохранения
    if (saveTaskBtn) {
        console.log('Добавление обработчика для кнопки сохранения');
        saveTaskBtn.addEventListener('click', function() {
            console.log('Кнопка сохранения нажата');
            submitTaskForm();
        });
    }
    
    // Фильтры
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function() {
            console.log(`Поиск: ${searchInput.value}`);
            filterTasks();
        }, 300));
    }
    
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            console.log(`Фильтр статуса: ${statusFilter.value}`);
            filterTasks();
        });
    }
    
    if (priorityFilter) {
        priorityFilter.addEventListener('change', function() {
            console.log(`Фильтр приоритета: ${priorityFilter.value}`);
            filterTasks();
        });
    }
    
    console.log('Обработчики событий настроены');
}

// Обработчик клика по кнопке добавления задачи
function handleAddTaskClick(event) {
    console.log('Обработка клика по кнопке добавления задачи');
    event.preventDefault();
    resetTaskForm();
    loadEmployeesList();
    loadVehiclesList();
    openTaskModal();
}

// Обработчик клика по кнопке закрытия модального окна
function handleCloseModalClick(event) {
    console.log('Обработка клика по кнопке закрытия модального окна');
    event.preventDefault();
    closeTaskModal();
}

// Открытие модального окна
function openTaskModal() {
    console.log('Открытие модального окна');
    if (!taskModal) {
        console.error('Модальное окно не найдено!');
        return;
    }
    
    // Устанавливаем текущую дату и время по умолчанию для срока выполнения
    const dueDateInput = taskForm.querySelector('[name="due_date"]');
    if (dueDateInput) {
        const now = new Date();
        now.setHours(now.getHours() + 24); // По умолчанию +24 часа от текущего времени
        const formattedDate = now.toISOString().slice(0, 16); // Формат: YYYY-MM-DDTHH:MM
        dueDateInput.value = formattedDate;
    }
    
    taskModal.classList.remove('hidden');
    console.log('Модальное окно открыто');
}

// Закрытие модального окна
function closeTaskModal() {
    console.log('Закрытие модального окна');
    if (!taskModal) {
        console.error('Модальное окно не найдено!');
        return;
    }
    
    taskModal.classList.add('hidden');
    console.log('Модальное окно закрыто');
}

// Сброс формы
function resetTaskForm() {
    console.log('Сброс формы задачи');
    if (!taskForm) {
        console.error('Форма задачи не найдена!');
        return;
    }
    
    taskForm.reset();
    
    // Установка заголовка модального окна
    if (modalTitle) {
        modalTitle.textContent = 'Новая задача';
    }
    
    // Сброс скрытого поля ID
    const taskIdInput = taskForm.querySelector('[name="task_id"]');
    if (taskIdInput) {
        taskIdInput.value = '';
    }
    
    console.log('Форма задачи сброшена');
}

// Загрузка списка сотрудников
async function loadEmployeesList() {
    console.log('Загрузка списка сотрудников');
    if (!taskForm) {
        console.error('Форма задачи не найдена!');
        return;
    }
    
    const selectElement = taskForm.querySelector('[name="assigned_to"]');
    const debugElement = document.getElementById('employeesDebug');
    
    if (!selectElement) {
        console.error('Поле выбора сотрудника не найдено!');
        if (debugElement) debugElement.textContent = 'Ошибка: Поле выбора сотрудника не найдено!';
        return;
    }
    
    // Показываем загрузку
    selectElement.disabled = true;
    if (debugElement) debugElement.textContent = 'Загрузка списка сотрудников...';
    
    try {
        // Используем только один проверенный URL
        console.log('Запрос списка сотрудников: /api/users/');
        const response = await fetch('/api/users/');
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        const responseText = await response.text();
        console.log('Ответ API (длина):', responseText.length);
        if (debugElement) debugElement.textContent = `Получен ответ: ${responseText.length} символов`;
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Ошибка парсинга JSON:', e);
            if (debugElement) debugElement.textContent = 'Ошибка: Некорректный формат ответа от сервера';
            throw new Error('Получен некорректный JSON от сервера');
        }
        
        console.log('Данные сотрудников:', data);
        if (debugElement) debugElement.textContent = `Загружено ${data.length} сотрудников`;
        
        // Очищаем список и добавляем опцию "Выберите сотрудника"
        selectElement.innerHTML = '<option value="">Выберите сотрудника</option>';
        
        // Заполняем список сотрудниками из API
        data.forEach(emp => {
            const option = document.createElement('option');
            option.value = emp.id;
            const fullName = `${emp.first_name || ''} ${emp.last_name || ''}`.trim();
            option.textContent = fullName || emp.username || `Сотрудник #${emp.id}`;
            selectElement.appendChild(option);
        });
        
        console.log(`Добавлено ${data.length} сотрудников в список`);
        
    } catch (error) {
        console.error('Ошибка при загрузке списка сотрудников:', error);
        if (debugElement) debugElement.textContent = `Ошибка: ${error.message}`;
        
        // Очищаем список
        selectElement.innerHTML = '<option value="">Выберите сотрудника</option>';
        
        // Добавляем тестовых сотрудников в случае ошибки
        console.warn('Добавление тестовых сотрудников из-за ошибки API');
        
        const testEmployees = [
            { id: 1, name: 'Тестовый сотрудник 1' },
            { id: 2, name: 'Тестовый сотрудник 2' },
            { id: 3, name: 'Тестовый сотрудник 3' }
        ];
        
        testEmployees.forEach(emp => {
            const option = document.createElement('option');
            option.value = emp.id;
            option.textContent = emp.name;
            selectElement.appendChild(option);
        });
    } finally {
        // Включаем элемент обратно
        selectElement.disabled = false;
    }
}

// Загрузка списка транспортных средств
async function loadVehiclesList() {
    console.log('Загрузка списка транспортных средств');
    if (!taskForm) {
        console.error('Форма задачи не найдена!');
        return;
    }
    
    const selectElement = taskForm.querySelector('[name="vehicle"]');
    const debugElement = document.getElementById('vehiclesDebug');
    
    if (!selectElement) {
        console.error('Поле выбора транспорта не найдено!');
        if (debugElement) debugElement.textContent = 'Ошибка: Поле выбора транспорта не найдено!';
        return;
    }
    
    // Показываем загрузку
    selectElement.disabled = true;
    if (debugElement) debugElement.textContent = 'Загрузка списка транспорта...';
    
    try {
        console.log('Запрос списка транспорта: /api/vehicles/');
        const response = await fetch('/api/vehicles/');
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        const responseText = await response.text();
        console.log('Ответ API транспорта (длина):', responseText.length);
        if (debugElement) debugElement.textContent = `Получен ответ: ${responseText.length} символов`;
        
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (e) {
            console.error('Ошибка парсинга JSON:', e);
            if (debugElement) debugElement.textContent = 'Ошибка: Некорректный формат ответа от сервера';
            throw new Error('Получен некорректный JSON от сервера');
        }
        
        console.log('Данные транспорта:', data);
        
        // Проверка структуры данных и извлечение списка транспортных средств
        const vehicles = Array.isArray(data) ? data : (data.results || []);
        if (debugElement) debugElement.textContent = `Загружено ${vehicles.length} транспортных средств`;
        
        // Очищаем список и добавляем опцию "Выберите транспорт"
        selectElement.innerHTML = '<option value="">Выберите транспорт</option>';
        
        // Заполняем список транспортными средствами из API
        vehicles.forEach(vehicle => {
            const option = document.createElement('option');
            option.value = vehicle.id;
            const vehicleText = vehicle.number ? 
                `${vehicle.number} (${vehicle.brand || ''} ${vehicle.model || ''})`.trim() : 
                `Транспорт #${vehicle.id}`;
            option.textContent = vehicleText;
            selectElement.appendChild(option);
        });
        
        console.log(`Добавлено ${vehicles.length} транспортных средств в список`);
        
    } catch (error) {
        console.error('Ошибка при загрузке списка транспорта:', error);
        if (debugElement) debugElement.textContent = `Ошибка: ${error.message}`;
        
        // Очищаем список
        selectElement.innerHTML = '<option value="">Выберите транспорт</option>';
        
        // Добавляем тестовые транспортные средства в случае ошибки
        console.warn('Добавление тестовых транспортных средств из-за ошибки API');
        
        const testVehicles = [
            { id: 1, name: 'Тестовый транспорт 1' },
            { id: 2, name: 'Тестовый транспорт 2' },
            { id: 3, name: 'Тестовый транспорт 3' }
        ];
        
        testVehicles.forEach(vehicle => {
            const option = document.createElement('option');
            option.value = vehicle.id;
            option.textContent = vehicle.name;
            selectElement.appendChild(option);
        });
    } finally {
        // Включаем элемент обратно
        selectElement.disabled = false;
    }
}

// Отправка формы задачи
async function submitTaskForm() {
    console.log('Отправка формы задачи');
    if (!taskForm) {
        console.error('Форма задачи не найдена!');
        return;
    }
    
    try {
        // Получаем CSRF токен из куки
        const csrfToken = getCookie('csrftoken');
        if (!csrfToken) {
            console.error('CSRF токен не найден!');
            alert('Ошибка безопасности: CSRF токен не найден. Пожалуйста, обновите страницу.');
            return;
        }
        
        console.log('Получен CSRF токен:', csrfToken);
        
        // Собираем данные формы
        const formData = new FormData(taskForm);
        const taskData = {};
        
        // Преобразуем FormData в объект
        for (let [key, value] of formData.entries()) {
            taskData[key] = value;
        }
        
        // Убираем пустые поля
        Object.keys(taskData).forEach(key => {
            if (taskData[key] === '') {
                delete taskData[key];
            }
        });
        
        console.log('Данные задачи для отправки:', taskData);
        
        // Проверяем обязательные поля
        if (!taskData.title) {
            alert('Пожалуйста, введите название задачи');
            return;
        }
        
        if (!taskData.due_date) {
            alert('Пожалуйста, укажите срок выполнения');
            return;
        }
        
        // Определяем URL для запроса
        const taskId = formData.get('task_id');
        const url = taskId ? `/api/tasks/${taskId}/` : '/api/tasks/';
        const method = taskId ? 'PUT' : 'POST';
        
        console.log(`Отправка ${method} запроса на URL: ${url}`);
        
        // Отправляем запрос
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(taskData)
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Ошибка при сохранении задачи:', errorText);
            throw new Error(`Ошибка при сохранении задачи: ${response.status} ${response.statusText}`);
        }
        
        const result = await response.json();
        console.log('Задача успешно сохранена:', result);
        
        // Закрываем модальное окно и обновляем список задач
        closeTaskModal();
        loadTasks();
        
        // Показываем уведомление об успешном сохранении
        alert('Задача успешно сохранена!');
        
    } catch (error) {
        console.error('Ошибка при отправке формы:', error);
        alert(`Ошибка при сохранении задачи: ${error.message}`);
    }
}

// Функция для получения CSRF токена из куки
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Загрузка задач
async function loadTasks() {
    console.log('Загрузка списка задач');
    if (!tasksList) {
        console.error('Список задач не найден!');
        return;
    }
    
    if (!loadingIndicator) {
        console.error('Индикатор загрузки не найден!');
    } else {
        loadingIndicator.classList.remove('hidden');
    }
    
    if (tasksList) tasksList.classList.add('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    
    // Добавляем отладочный элемент на страницу
    let debugDiv = document.getElementById('tasksDebug');
    if (!debugDiv) {
        debugDiv = document.createElement('div');
        debugDiv.id = 'tasksDebug';
        debugDiv.className = 'bg-gray-100 p-4 mb-4 rounded text-xs';
        tasksList.parentNode.insertBefore(debugDiv, tasksList);
    }
    debugDiv.innerHTML = 'Загрузка задач...';
    
    try {
        // Получаем CSRF токен для авторизации
        const csrfToken = getCookie('csrftoken');
        
        debugDiv.innerHTML += '<br>Отправка запроса на /api/tasks/';
        console.log('Запрос задач: /api/tasks/');
        
        const response = await fetch('/api/tasks/', {
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin' // Включаем куки в запрос
        });
        
        debugDiv.innerHTML += `<br>Ответ получен: статус ${response.status}`;
        console.log('Статус ответа:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            debugDiv.innerHTML += `<br>Ошибка: ${errorText}`;
            throw new Error(`Ошибка HTTP: ${response.status}, ${errorText}`);
        }
        
        // Сначала получаем текст ответа для отладки
        const responseText = await response.text();
        debugDiv.innerHTML += `<br>Ответ (длина): ${responseText.length} символов`;
        console.log('Текст ответа (длина):', responseText.length);
        
        // Пытаемся распарсить JSON
        try {
            const data = JSON.parse(responseText);
            console.log('Данные задач:', data);
            
            // Проверяем структуру данных
            if (Array.isArray(data)) {
                tasks = data;
                debugDiv.innerHTML += `<br>Получено ${tasks.length} задач (массив)`;
            } else if (data.results && Array.isArray(data.results)) {
                tasks = data.results;
                debugDiv.innerHTML += `<br>Получено ${tasks.length} задач (пагинация)`;
            } else {
                debugDiv.innerHTML += `<br>Структура данных неизвестна: ${JSON.stringify(data).substring(0, 100)}...`;
                tasks = [];
            }
            
            // Показываем первые несколько задач для отладки
            if (tasks.length > 0) {
                debugDiv.innerHTML += `<br>Пример задачи: ${JSON.stringify(tasks[0]).substring(0, 200)}...`;
            }
            
            console.log(`Загружено ${tasks.length} задач`);
            
            // Фильтруем и отображаем задачи
            filterTasks();
            
        } catch (parseError) {
            console.error('Ошибка парсинга JSON:', parseError);
            debugDiv.innerHTML += `<br>Ошибка парсинга JSON: ${parseError.message}`;
            debugDiv.innerHTML += `<br>Начало ответа: ${responseText.substring(0, 100)}...`;
            throw parseError;
        }
        
    } catch (error) {
        console.error('Ошибка при загрузке задач:', error);
        debugDiv.innerHTML += `<br>Ошибка: ${error.message}`;
        
        if (emptyState) emptyState.classList.remove('hidden');
        if (tasksList) tasksList.classList.add('hidden');
    } finally {
        if (loadingIndicator) loadingIndicator.classList.add('hidden');
    }
}

// Фильтрация и отображение задач
function filterTasks() {
    console.log('Фильтрация задач');
    
    // Используем отладочный элемент
    let debugDiv = document.getElementById('tasksDebug');
    if (debugDiv) {
        debugDiv.innerHTML += '<br>Начало фильтрации задач';
    }
    
    if (!tasksList) {
        console.error('Список задач не найден!');
        if (debugDiv) debugDiv.innerHTML += '<br>Ошибка: Список задач не найден!';
        return;
    }
    
    // Применяем фильтры
    console.log('Исходное количество задач:', tasks.length);
    if (debugDiv) debugDiv.innerHTML += `<br>Исходное количество задач: ${tasks.length}`;
    
    let filteredTasks = [...tasks];
    
    const searchQuery = searchInput ? searchInput.value.toLowerCase() : '';
    const statusValue = statusFilter ? statusFilter.value : '';
    const priorityValue = priorityFilter ? priorityFilter.value : '';
    
    if (debugDiv) {
        debugDiv.innerHTML += `<br>Фильтры: поиск="${searchQuery}", статус="${statusValue}", приоритет="${priorityValue}"`;
    }
    
    if (searchQuery) {
        filteredTasks = filteredTasks.filter(task => 
            (task.title && task.title.toLowerCase().includes(searchQuery)) || 
            (task.description && task.description.toLowerCase().includes(searchQuery))
        );
    }
    
    if (statusValue) {
        filteredTasks = filteredTasks.filter(task => task.status === statusValue);
    }
    
    if (priorityValue) {
        filteredTasks = filteredTasks.filter(task => task.priority === priorityValue);
    }
    
    console.log(`Отфильтровано ${filteredTasks.length} задач из ${tasks.length}`);
    if (debugDiv) debugDiv.innerHTML += `<br>После фильтрации: ${filteredTasks.length} задач`;
    
    // Отображаем результаты
    if (filteredTasks.length === 0) {
        if (tasksList) tasksList.classList.add('hidden');
        if (emptyState) emptyState.classList.remove('hidden');
        if (debugDiv) debugDiv.innerHTML += '<br>Нет задач для отображения, показываем пустое состояние';
        return;
    }
    
    if (tasksList) tasksList.classList.remove('hidden');
    if (emptyState) emptyState.classList.add('hidden');
    
    // Формируем HTML для списка задач
    if (debugDiv) debugDiv.innerHTML += '<br>Формирование HTML для списка задач';
    
    let tasksHTML = '';
    
    filteredTasks.forEach(task => {
        // Безопасный доступ к свойствам
        const title = task.title || 'Без названия';
        const description = task.description || 'Нет описания';
        const status = task.status || 'NEW';
        const priority = task.priority || 'MEDIUM';
        const dueDate = task.due_date || '';
        const createdAt = task.created_at || '';
        
        const assignedToName = task.assigned_user_details ?
            `${task.assigned_user_details.first_name || ''} ${task.assigned_user_details.last_name || ''}`.trim() || 'Не назначено' :
            'Не назначено';
        
        const vehicleDetails = task.vehicle_details ? 
            `${task.vehicle_details.brand || ''} ${task.vehicle_details.model || ''}`.trim() || 'Не указано' : 
            'Не указано';
        
        tasksHTML += `
            <div class="bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-shadow mb-4">
                <div class="flex items-start justify-between">
                    <div class="flex-1">
                        <div class="flex items-center space-x-2 mb-2">
                            <h3 class="font-medium text-gray-800">${title}</h3>
                            <span class="px-2 py-1 text-xs rounded-full ${getStatusStyle(status)}">${getStatusText(status)}</span>
                            <span class="px-2 py-1 text-xs rounded-full ${getPriorityStyle(priority)}">${getPriorityText(priority)}</span>
                        </div>
                        <p class="text-gray-600 text-sm mb-4">${description}</p>
                        <div class="grid grid-cols-2 gap-4 text-sm text-gray-600">
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-user text-gray-400"></i>
                                <span>${assignedToName}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-truck text-gray-400"></i>
                                <span>${vehicleDetails}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-clock text-gray-400"></i>
                                <span>До ${formatDate(dueDate)}</span>
                            </div>
                            <div class="flex items-center space-x-2">
                                <i class="fas fa-calendar text-gray-400"></i>
                                <span>Создано ${formatDate(createdAt)}</span>
                            </div>
                        </div>
                    </div>
                    <div class="flex space-x-2">
                        <button type="button" 
                            onclick="editTask(${task.id})" 
                            class="p-2 text-blue-600 hover:text-blue-800">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" 
                            onclick="changeTaskStatus(${task.id})" 
                            class="p-2 text-green-600 hover:text-green-800">
                            <i class="fas fa-check"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    tasksList.innerHTML = tasksHTML;
    
    if (debugDiv) debugDiv.innerHTML += `<br>Отрисовано ${filteredTasks.length} задач`;
}

// Редактирование задачи
window.editTask = async function(taskId) {
    console.log(`Редактирование задачи с ID: ${taskId}`);
    
    if (!taskForm || !taskModal) {
        console.error('Необходимые элементы страницы не найдены!');
        return;
    }
    
    // Находим задачу по ID
    const task = tasks.find(t => t.id === taskId);
    if (!task) {
        console.error(`Задача с ID ${taskId} не найдена`);
        return;
    }
    
    // Устанавливаем ID редактируемой задачи
    currentTaskId = taskId;
    
    const modalTitle = document.getElementById('modalTitle');
    if (modalTitle) {
        modalTitle.textContent = 'Редактировать задачу';
    }
    
    // Загружаем списки
    await Promise.all([loadEmployeesList(), loadVehiclesList()]);
    
    // Заполняем форму данными задачи
    taskForm.title.value = task.title || '';
    taskForm.description.value = task.description || '';
    taskForm.priority.value = task.priority || 'MEDIUM';
    
    // Форматируем дату к формату datetime-local
    if (task.due_date) {
        const dueDate = new Date(task.due_date);
        const isoDate = dueDate.toISOString().slice(0, 16);
        taskForm.due_date.value = isoDate;
    }
    
    // Устанавливаем значения после загрузки списков
    setTimeout(() => {
        taskForm.assigned_to.value = task.assigned_to || '';
        taskForm.vehicle.value = task.vehicle || '';
    }, 500);
    
    // Открываем модальное окно
    taskModal.classList.remove('hidden');
};

// Изменение статуса задачи
window.changeTaskStatus = async function(taskId) {
    console.log(`Изменение статуса задачи с ID: ${taskId}`);
    
    // Находим задачу по ID
    const task = tasks.find(t => t.id === taskId);
    if (!task) {
        console.error(`Задача с ID ${taskId} не найдена`);
        return;
    }
    
    // Определяем следующий статус
    let newStatus;
    switch (task.status) {
        case 'NEW': newStatus = 'IN_PROGRESS'; break;
        case 'IN_PROGRESS': newStatus = 'COMPLETED'; break;
        default: 
            console.log(`Для статуса ${task.status} нет следующего шага`);
            return;
    }
    
    try {
        // Получаем CSRF-токен
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        if (!csrfToken) {
            console.error('CSRF-токен не найден!');
            alert('Ошибка безопасности: CSRF-токен не найден!');
            return;
        }
        
        // Отправляем запрос на изменение статуса
        const response = await fetch(`/api/tasks/${taskId}/change_status/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Ошибка при изменении статуса');
        }
        
        // Обновляем список задач
        await loadTasks();
        
    } catch (error) {
        console.error('Ошибка при изменении статуса:', error);
        alert(`Ошибка: ${error.message}`);
    }
};

// Вспомогательные функции
function formatDate(dateString) {
    if (!dateString) return '';
    return new Date(dateString).toLocaleString('ru');
}

function getStatusStyle(status) {
    switch (status) {
        case 'NEW': return 'bg-blue-100 text-blue-800';
        case 'IN_PROGRESS': return 'bg-yellow-100 text-yellow-800';
        case 'COMPLETED': return 'bg-green-100 text-green-800';
        case 'CANCELLED': return 'bg-gray-100 text-gray-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

function getStatusText(status) {
    switch (status) {
        case 'NEW': return 'Новая';
        case 'IN_PROGRESS': return 'В работе';
        case 'COMPLETED': return 'Завершена';
        case 'CANCELLED': return 'Отменена';
        default: return status;
    }
}

function getPriorityStyle(priority) {
    switch (priority) {
        case 'HIGH': return 'bg-red-100 text-red-800';
        case 'MEDIUM': return 'bg-orange-100 text-orange-800';
        case 'LOW': return 'bg-green-100 text-green-800';
        default: return 'bg-gray-100 text-gray-800';
    }
}

function getPriorityText(priority) {
    switch (priority) {
        case 'HIGH': return 'Высокий';
        case 'MEDIUM': return 'Средний';
        case 'LOW': return 'Низкий';
        default: return priority;
    }
}

function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
} 