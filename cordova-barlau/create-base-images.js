const fs = require('fs');
const { createCanvas } = require('canvas');

// Создаем иконку 1024x1024
function createIcon() {
    const canvas = createCanvas(1024, 1024);
    const ctx = canvas.getContext('2d');
    
    // Фон
    const gradient = ctx.createLinearGradient(0, 0, 1024, 1024);
    gradient.addColorStop(0, '#2563EB');
    gradient.addColorStop(1, '#1E40AF');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 1024, 1024);
    
    // Круг в центре
    const centerX = 1024 / 2;
    const centerY = 1024 / 2;
    const radius = 1024 * 0.35;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fill();
    
    // Текст
    ctx.fillStyle = '#1E40AF';
    ctx.font = 'bold 150px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('B', centerX, centerY);
    
    // Внешнее кольцо
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 1.2, 0, 2 * Math.PI, false);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.lineWidth = 30;
    ctx.stroke();
    
    // Сохраняем изображение
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync('icon-1024.png', buffer);
    console.log('Иконка создана: icon-1024.png');
}

// Создаем заставку 2732x2732 (квадратную, для последующей обрезки)
function createSplash() {
    const canvas = createCanvas(2732, 2732);
    const ctx = canvas.getContext('2d');
    
    // Фон
    const gradient = ctx.createLinearGradient(0, 0, 2732, 2732);
    gradient.addColorStop(0, '#2563EB');
    gradient.addColorStop(1, '#1E40AF');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 2732, 2732);
    
    // Лого (такое же как на иконке, но меньше)
    const centerX = 2732 / 2;
    const centerY = 2732 / 2 - 2732 * 0.05;
    const radius = 2732 * 0.2;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fill();
    
    ctx.fillStyle = '#1E40AF';
    ctx.font = 'bold 220px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('B', centerX, centerY);
    
    // Внешнее кольцо
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 1.2, 0, 2 * Math.PI, false);
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.lineWidth = 54;
    ctx.stroke();
    
    // Текст BARLAU.KZ
    ctx.fillStyle = 'white';
    ctx.font = 'bold 164px Arial';
    ctx.fillText('BARLAU.KZ', centerX, centerY + radius * 2);
    
    // Подзаголовок
    ctx.font = '82px Arial';
    ctx.fillText('Система управления логистикой', centerX, centerY + radius * 2.5);
    
    // Сохраняем изображение
    const buffer = canvas.toBuffer('image/png');
    fs.writeFileSync('splash.png', buffer);
    console.log('Заставка создана: splash.png');
}

// Выполняем обе функции
createIcon();
createSplash();

console.log('Базовые изображения созданы успешно!'); 
 