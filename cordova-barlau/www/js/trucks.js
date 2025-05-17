/**
 * BARLAU.KZ Mobile App - Модуль для работы с грузовиками
 * Обеспечивает локальное хранение и управление данными о грузовиках
 */

const TrucksModule = {
    // Локальное хранилище данных
    storage: window.localStorage,
    
    // Ключ для хранения данных в localStorage
    storageKey: 'barlau_trucks_data',
    
    // Метод для получения всех грузовиков
    getAllTrucks: function() {
        const trucksData = this.storage.getItem(this.storageKey);
        if (trucksData) {
            try {
                return JSON.parse(trucksData);
            } catch (e) {
                console.error('Ошибка при парсинге данных о грузовиках:', e);
                return [];
            }
        }
        return [];
    },
    
    // Метод для получения данных о конкретном грузовике
    getTruckById: function(id) {
        const trucks = this.getAllTrucks();
        return trucks.find(truck => truck.id === id) || null;
    },
    
    // Метод для сохранения всех данных
    saveAllTrucks: function(trucks) {
        try {
            this.storage.setItem(this.storageKey, JSON.stringify(trucks));
            return true;
        } catch (e) {
            console.error('Ошибка при сохранении данных о грузовиках:', e);
            return false;
        }
    },
    
    // Метод для добавления нового грузовика
    addTruck: function(truck) {
        const trucks = this.getAllTrucks();
        // Генерируем ID для нового грузовика
        const newId = trucks.length > 0 ? Math.max(...trucks.map(t => t.id)) + 1 : 1;
        truck.id = newId;
        
        // Добавляем дополнительные поля, если их нет
        if (!truck.documents) truck.documents = [];
        if (!truck.history) truck.history = [];
        if (!truck.photos) truck.photos = [];
        
        trucks.push(truck);
        return this.saveAllTrucks(trucks) ? truck : null;
    },
    
    // Метод для обновления существующего грузовика
    updateTruck: function(truck) {
        const trucks = this.getAllTrucks();
        const index = trucks.findIndex(t => t.id === truck.id);
        
        if (index === -1) return null;
        
        trucks[index] = truck;
        return this.saveAllTrucks(trucks) ? truck : null;
    },
    
    // Метод для удаления грузовика
    deleteTruck: function(id) {
        const trucks = this.getAllTrucks();
        const updatedTrucks = trucks.filter(truck => truck.id !== id);
        
        if (trucks.length === updatedTrucks.length) return false;
        
        return this.saveAllTrucks(updatedTrucks);
    },
    
    // Метод для добавления документа к грузовику
    addDocument: function(truckId, document) {
        const truck = this.getTruckById(truckId);
        if (!truck) return false;
        
        // Генерируем ID для нового документа
        const newId = truck.documents.length > 0 ? 
            Math.max(...truck.documents.map(d => d.id)) + 1 : 1;
        document.id = newId;
        
        truck.documents.push(document);
        return this.updateTruck(truck) ? document : null;
    },
    
    // Метод для обновления документа
    updateDocument: function(truckId, document) {
        const truck = this.getTruckById(truckId);
        if (!truck) return false;
        
        const index = truck.documents.findIndex(d => d.id === document.id);
        if (index === -1) return false;
        
        truck.documents[index] = document;
        return this.updateTruck(truck) ? document : null;
    },
    
    // Метод для удаления документа
    deleteDocument: function(truckId, documentId) {
        const truck = this.getTruckById(truckId);
        if (!truck) return false;
        
        const originalLength = truck.documents.length;
        truck.documents = truck.documents.filter(d => d.id !== documentId);
        
        if (originalLength === truck.documents.length) return false;
        
        return this.updateTruck(truck);
    },
    
    // Метод для добавления записи в историю
    addHistoryRecord: function(truckId, record) {
        const truck = this.getTruckById(truckId);
        if (!truck) return false;
        
        truck.history.push(record);
        // Сортируем историю по дате в убывающем порядке
        truck.history.sort((a, b) => new Date(b.date) - new Date(a.date));
        
        return this.updateTruck(truck) ? record : null;
    },
    
    // Метод для добавления фотографии
    addPhoto: function(truckId, photoUrl) {
        const truck = this.getTruckById(truckId);
        if (!truck) return false;
        
        truck.photos.push(photoUrl);
        return this.updateTruck(truck) ? photoUrl : null;
    },
    
    // Метод для удаления фотографии
    deletePhoto: function(truckId, photoIndex) {
        const truck = this.getTruckById(truckId);
        if (!truck || photoIndex < 0 || photoIndex >= truck.photos.length) return false;
        
        truck.photos.splice(photoIndex, 1);
        return this.updateTruck(truck);
    },
    
    // Метод для проверки истекающих документов
    getExpiringDocuments: function(daysThreshold = 30) {
        const trucks = this.getAllTrucks();
        const today = new Date();
        const expiringDocs = [];
        
        trucks.forEach(truck => {
            if (!truck.documents) return;
            
            truck.documents.forEach(doc => {
                if (!doc.expiration) return;
                
                const expDate = new Date(doc.expiration);
                const diffTime = expDate - today;
                const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (diffDays <= daysThreshold && diffDays >= 0) {
                    expiringDocs.push({
                        truckId: truck.id,
                        truckName: truck.name,
                        document: doc,
                        daysLeft: diffDays
                    });
                }
            });
        });
        
        return expiringDocs;
    },
    
    // Метод для получения документов с истекшим сроком
    getExpiredDocuments: function() {
        const trucks = this.getAllTrucks();
        const today = new Date();
        const expiredDocs = [];
        
        trucks.forEach(truck => {
            if (!truck.documents) return;
            
            truck.documents.forEach(doc => {
                if (!doc.expiration) return;
                
                const expDate = new Date(doc.expiration);
                if (expDate < today) {
                    expiredDocs.push({
                        truckId: truck.id,
                        truckName: truck.name,
                        document: doc,
                        daysExpired: Math.ceil((today - expDate) / (1000 * 60 * 60 * 24))
                    });
                }
            });
        });
        
        return expiredDocs;
    },
    
    // Метод для инициализации демо-данных (для разработки)
    initDemoData: function() {
        // Проверяем, есть ли уже данные
        if (this.getAllTrucks().length > 0) {
            console.log('Демо-данные уже загружены');
            return;
        }
        
        const demoTrucks = [
            {
                id: 1,
                name: "Volvo FH16",
                model: "Volvo FH16 750",
                year: 2020,
                registration: "A123BC",
                status: "active",
                image: "https://via.placeholder.com/300x200?text=Volvo+FH16",
                dimensions: "16.5×2.6×4.0 м",
                capacity: "44 тонны",
                volume: "92 м³",
                bodyType: "Тентованный полуприцеп",
                mileage: "120000 км",
                notes: "В отличном состоянии, недавно пройден техосмотр.",
                documents: [
                    {
                        id: 1,
                        title: "Страховой полис ОСАГО",
                        date: "2023-05-15",
                        expiration: "2024-05-15",
                        status: "valid"
                    },
                    {
                        id: 2,
                        title: "Технический осмотр",
                        date: "2023-01-10",
                        expiration: "2023-07-10",
                        status: "expiring"
                    },
                    {
                        id: 3,
                        title: "Международное разрешение",
                        date: "2022-10-20",
                        expiration: "2023-01-20",
                        status: "expired"
                    }
                ],
                history: [
                    {
                        date: "2023-05-20",
                        description: "Плановое техническое обслуживание. Замена масла и фильтров."
                    },
                    {
                        date: "2023-03-15",
                        description: "Замена передних тормозных колодок."
                    },
                    {
                        date: "2022-12-10",
                        description: "Сезонное обслуживание, замена шин на зимние."
                    }
                ],
                photos: [
                    "https://via.placeholder.com/150?text=Фото+1",
                    "https://via.placeholder.com/150?text=Фото+2",
                    "https://via.placeholder.com/150?text=Фото+3",
                    "https://via.placeholder.com/150?text=Фото+4"
                ]
            },
            {
                id: 2,
                name: "Mercedes Actros",
                model: "Mercedes Actros 1845",
                year: 2019,
                registration: "E456FG",
                status: "idle",
                image: "https://via.placeholder.com/300x200?text=Mercedes+Actros",
                dimensions: "16.0×2.5×4.0 м",
                capacity: "40 тонн",
                volume: "86 м³",
                bodyType: "Тентованный полуприцеп",
                mileage: "180000 км",
                notes: "Требуется плановое обслуживание в ближайшее время.",
                documents: [],
                history: [],
                photos: []
            },
            {
                id: 3,
                name: "Scania R500",
                model: "Scania R500 V8",
                year: 2021,
                registration: "H789IJ",
                status: "maintenance",
                image: "https://via.placeholder.com/300x200?text=Scania+R500",
                dimensions: "16.8×2.6×4.0 м",
                capacity: "44 тонны",
                volume: "98 м³",
                bodyType: "Рефрижератор",
                mileage: "75000 км",
                notes: "На техобслуживании до 25.06.2023, замена трансмиссии.",
                documents: [],
                history: [],
                photos: []
            }
        ];
        
        this.saveAllTrucks(demoTrucks);
        console.log('Демо-данные успешно загружены');
    },
    
    // Метод для кэширования изображения
    cacheImage: function(url) {
        return new Promise((resolve, reject) => {
            // Проверяем, поддерживается ли Service Worker
            if (!('serviceWorker' in navigator) || !navigator.serviceWorker.controller) {
                console.warn('Service Worker не инициализирован');
                reject(new Error('Service Worker не инициализирован'));
                return;
            }
            
            // Устанавливаем обработчик сообщений от Service Worker
            const messageHandler = (event) => {
                if (event.data && event.data.type === 'IMAGE_CACHED' && event.data.url === url) {
                    // Удаляем обработчик после получения ответа
                    navigator.serviceWorker.removeEventListener('message', messageHandler);
                    
                    if (event.data.success) {
                        resolve(url);
                    } else {
                        reject(new Error(event.data.error || 'Ошибка кэширования'));
                    }
                }
            };
            
            navigator.serviceWorker.addEventListener('message', messageHandler);
            
            // Отправляем сообщение в Service Worker для кэширования
            navigator.serviceWorker.controller.postMessage({
                type: 'CACHE_IMAGE',
                url: url
            });
            
            // Таймаут на случай, если ответ не придет
            setTimeout(() => {
                navigator.serviceWorker.removeEventListener('message', messageHandler);
                reject(new Error('Таймаут кэширования изображения'));
            }, 10000);
        });
    },
    
    // Метод для кэширования всех изображений грузовиков
    cacheAllTruckImages: function() {
        const trucks = this.getAllTrucks();
        const promises = [];
        
        // Кэшируем основные изображения грузовиков
        trucks.forEach(truck => {
            if (truck.image) {
                promises.push(this.cacheImage(truck.image));
            }
            
            // Кэшируем дополнительные фотографии
            if (truck.photos && truck.photos.length > 0) {
                truck.photos.forEach(photoUrl => {
                    promises.push(this.cacheImage(photoUrl));
                });
            }
        });
        
        return Promise.allSettled(promises);
    },
    
    // Метод для обновления информации о грузовиках с сервера (заглушка)
    syncTrucksWithServer: function() {
        // Заглушка для демонстрации
        console.log('Синхронизация данных с сервером...');
        
        // Здесь будет реальная логика синхронизации с сервером
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Синхронизация завершена');
                // После синхронизации кэшируем все изображения
                this.cacheAllTruckImages()
                    .then(() => {
                        console.log('Все изображения кэшированы');
                    })
                    .catch(error => {
                        console.error('Ошибка кэширования изображений:', error);
                    });
                
                resolve({ success: true, message: 'Данные синхронизированы' });
            }, 2000);
        });
    },
    
    // Метод для подключения системы уведомлений об истекающих документах
    setupDocumentNotifications: function() {
        // Проверяем наличие плагина уведомлений
        if (!window.cordova || !window.cordova.plugins || !window.cordova.plugins.notification || !window.cordova.plugins.notification.local) {
            console.warn('Плагин уведомлений не доступен');
            return false;
        }
        
        // Получаем истекающие документы
        const expiringDocs = this.getExpiringDocuments();
        
        // Для каждого истекающего документа создаем уведомление
        expiringDocs.forEach((item, index) => {
            const notificationId = 1000 + index;
            
            window.cordova.plugins.notification.local.schedule({
                id: notificationId,
                title: `Истекает документ: ${item.document.title}`,
                text: `Для грузовика ${item.truckName} истекает срок документа через ${item.daysLeft} дней`,
                foreground: true,
                sound: true,
                trigger: { at: new Date(new Date().getTime() + 60 * 1000) } // Уведомление через минуту для тестирования
            });
        });
        
        return true;
    }
};

// Экспортируем модуль
window.TrucksModule = TrucksModule; 
 