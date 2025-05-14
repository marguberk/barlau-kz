const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

// Путь к изображениям
const SOURCE_ICON = path.join(__dirname, 'icon-1024.png');
const SOURCE_SPLASH = path.join(__dirname, 'splash.png');

// Конфигурация размеров иконок для iOS
const IOS_ICONS = [
    { name: 'icon-20.png', size: 20 },
    { name: 'icon-20@2x.png', size: 40 },
    { name: 'icon-20@3x.png', size: 60 },
    { name: 'icon-29.png', size: 29 },
    { name: 'icon-29@2x.png', size: 58 },
    { name: 'icon-29@3x.png', size: 87 },
    { name: 'icon-40.png', size: 40 },
    { name: 'icon-40@2x.png', size: 80 },
    { name: 'icon-40@3x.png', size: 120 },
    { name: 'icon-60@2x.png', size: 120 },
    { name: 'icon-60@3x.png', size: 180 },
    { name: 'icon-76.png', size: 76 },
    { name: 'icon-76@2x.png', size: 152 },
    { name: 'icon-83.5@2x.png', size: 167 },
    { name: 'icon-1024.png', size: 1024 }
];

// Конфигурация размеров иконок для Android
const ANDROID_ICONS = [
    { name: 'ldpi.png', size: 36 },
    { name: 'mdpi.png', size: 48 },
    { name: 'hdpi.png', size: 72 },
    { name: 'xhdpi.png', size: 96 },
    { name: 'xxhdpi.png', size: 144 },
    { name: 'xxxhdpi.png', size: 192 }
];

// Конфигурация размеров заставок для iOS
const IOS_SPLASHES = [
    { name: 'splash-Default@2x~iphone.png', width: 640, height: 960 },
    { name: 'splash-Default-568h@2x~iphone.png', width: 640, height: 1136 },
    { name: 'splash-Default-667h.png', width: 750, height: 1334 },
    { name: 'splash-Default-736h.png', width: 1242, height: 2208 },
    { name: 'splash-Default-Landscape-736h.png', width: 2208, height: 1242 },
    { name: 'splash-Default-Portrait~ipad.png', width: 768, height: 1024 },
    { name: 'splash-Default-Landscape~ipad.png', width: 1024, height: 768 },
    { name: 'splash-Default-Portrait@2x~ipad.png', width: 1536, height: 2048 },
    { name: 'splash-Default-Landscape@2x~ipad.png', width: 2048, height: 1536 },
    { name: 'splash-1125x2436.png', width: 1125, height: 2436 },
    { name: 'splash-2436x1125.png', width: 2436, height: 1125 }
];

// Конфигурация размеров заставок для Android
const ANDROID_SPLASHES = [
    { name: 'splash-ldpi.png', width: 320, height: 426 },
    { name: 'splash-mdpi.png', width: 320, height: 470 },
    { name: 'splash-hdpi.png', width: 480, height: 640 },
    { name: 'splash-xhdpi.png', width: 720, height: 960 },
    { name: 'splash-xxhdpi.png', width: 960, height: 1280 },
    { name: 'splash-xxxhdpi.png', width: 1280, height: 1920 }
];

// Создаем директории, если их нет
const directories = [
    'res/ios',
    'res/android'
];

directories.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`Создана директория: ${dir}`);
    }
});

// Генерация иконок для iOS
console.log('Генерация иконок для iOS...');
IOS_ICONS.forEach(icon => {
    const outputPath = path.join(__dirname, 'res/ios', icon.name);
    sharp(SOURCE_ICON)
        .resize(icon.size, icon.size, { fit: 'contain' })
        .toFile(outputPath)
        .then(() => console.log(`Создана иконка: ${outputPath}`))
        .catch(err => console.error(`Ошибка при создании иконки ${icon.name}:`, err));
});

// Генерация иконок для Android
console.log('Генерация иконок для Android...');
ANDROID_ICONS.forEach(icon => {
    const outputPath = path.join(__dirname, 'res/android', icon.name);
    sharp(SOURCE_ICON)
        .resize(icon.size, icon.size, { fit: 'contain' })
        .toFile(outputPath)
        .then(() => console.log(`Создана иконка: ${outputPath}`))
        .catch(err => console.error(`Ошибка при создании иконки ${icon.name}:`, err));
});

// Функция для создания заставок
function createSplash(splash, platform) {
    const outputPath = path.join(__dirname, `res/${platform}`, splash.name);
    const maxDimension = Math.max(splash.width, splash.height);
    
    // Для генерации заставок использовать resize без extract
    sharp(SOURCE_SPLASH)
        .resize(splash.width, splash.height, { fit: 'cover' })
        .toFile(outputPath)
        .then(() => console.log(`Создана заставка: ${outputPath}`))
        .catch(err => console.error(`Ошибка при создании заставки ${splash.name}:`, err));
}

// Генерация заставок для iOS
console.log('Генерация заставок для iOS...');
IOS_SPLASHES.forEach(splash => {
    createSplash(splash, 'ios');
});

// Генерация заставок для Android
console.log('Генерация заставок для Android...');
ANDROID_SPLASHES.forEach(splash => {
    createSplash(splash, 'android');
});

console.log('Запуск генерации ресурсов завершен! Ожидание завершения обработки изображений...'); 
 