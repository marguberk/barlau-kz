// Утилиты для работы с классами (аналог cn функции)
function cn(...classes) {
  return classes
    .filter(Boolean)
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// Функции для создания вариантов компонентов
const buttonVariants = {
  variant: {
    default: 'btn btn-default btn-default-size',
    destructive: 'btn btn-destructive btn-default-size',
    outline: 'btn btn-outline btn-default-size',
    secondary: 'btn btn-secondary btn-default-size',
    ghost: 'btn btn-ghost btn-default-size',
    link: 'btn btn-link btn-default-size'
  },
  size: {
    default: 'btn-default-size',
    sm: 'btn-sm',
    lg: 'btn-lg',
    icon: 'btn-icon'
  }
};

const badgeVariants = {
  variant: {
    default: 'badge badge-default',
    secondary: 'badge badge-secondary',
    destructive: 'badge badge-destructive',
    outline: 'badge badge-outline'
  }
};

// Функция для применения вариантов кнопок
function getButtonClasses(variant = 'default', size = 'default', customClasses = '') {
  const baseClasses = 'btn';
  const variantClass = buttonVariants.variant[variant] || buttonVariants.variant.default;
  const sizeClass = buttonVariants.size[size] || '';
  
  return cn(baseClasses, variantClass, sizeClass, customClasses);
}

// Функция для применения вариантов значков
function getBadgeClasses(variant = 'default', customClasses = '') {
  const variantClass = badgeVariants.variant[variant] || badgeVariants.variant.default;
  return cn(variantClass, customClasses);
}

// Функция для создания карточек
function createCard({ title, description, content, footer, customClasses = '' }) {
  const cardHtml = `
    <div class="${cn('card', customClasses)}">
      ${title || description ? `
        <div class="card-header">
          ${title ? `<h3 class="card-title">${title}</h3>` : ''}
          ${description ? `<p class="card-description">${description}</p>` : ''}
        </div>
      ` : ''}
      ${content ? `<div class="card-content">${content}</div>` : ''}
      ${footer ? `<div class="card-footer">${footer}</div>` : ''}
    </div>
  `;
  return cardHtml;
}

// Функция для создания алертов
function createAlert({ title, description, variant = 'default', customClasses = '' }) {
  const alertClass = variant === 'destructive' ? 'alert alert-destructive' : 'alert alert-default';
  
  const alertHtml = `
    <div class="${cn(alertClass, customClasses)}">
      ${title ? `<h5 class="alert-title">${title}</h5>` : ''}
      ${description ? `<div class="alert-description">${description}</div>` : ''}
    </div>
  `;
  return alertHtml;
}

// Функция для работы с темой
function toggleTheme() {
  const html = document.documentElement;
  const currentTheme = html.classList.contains('dark') ? 'dark' : 'light';
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
  
  html.classList.remove(currentTheme);
  html.classList.add(newTheme);
  
  // Сохраняем предпочтение пользователя
  localStorage.setItem('theme', newTheme);
  
  return newTheme;
}

// Функция для установки темы при загрузке страницы
function initTheme() {
  const savedTheme = localStorage.getItem('theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = savedTheme || (prefersDark ? 'dark' : 'light');
  
  document.documentElement.classList.add(theme);
}

// Функция для анимации появления элементов
function animateElement(element, animationClass = 'animate-fade-in-up') {
  if (element) {
    element.classList.add(animationClass);
  }
}

// Функция для создания тостов (уведомлений)
function showToast({ title, description, variant = 'default', duration = 5000 }) {
  const toastContainer = document.getElementById('toast-container') || createToastContainer();
  
  const toast = document.createElement('div');
  toast.className = cn(
    'toast fixed bottom-4 right-4 z-50 max-w-sm p-4 rounded-lg shadow-lg',
    'animate-fade-in-up',
    variant === 'destructive' ? 'bg-destructive text-destructive-foreground' : 'bg-card text-card-foreground border'
  );
  
  toast.innerHTML = `
    <div class="flex items-start gap-2">
      <div class="flex-1">
        ${title ? `<div class="font-medium">${title}</div>` : ''}
        ${description ? `<div class="text-sm opacity-90">${description}</div>` : ''}
      </div>
      <button class="toast-close opacity-70 hover:opacity-100" onclick="this.parentElement.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `;
  
  toastContainer.appendChild(toast);
  
  // Автоматическое удаление
  if (duration > 0) {
    setTimeout(() => {
      if (toast.parentElement) {
        toast.remove();
      }
    }, duration);
  }
  
  return toast;
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  container.className = 'fixed bottom-4 right-4 z-50 flex flex-col gap-2';
  document.body.appendChild(container);
  return container;
}

// Функция для обработки форм Django
function enhanceDjangoForms() {
  // Применяем стили к формам Django
  document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], textarea, select').forEach(input => {
    if (!input.classList.contains('input')) {
      input.classList.add('input');
    }
  });
  
  // Применяем стили к кнопкам Django
  document.querySelectorAll('button[type="submit"], input[type="submit"]').forEach(button => {
    if (!button.classList.contains('btn')) {
      button.className = getButtonClasses('default', 'default', button.className);
    }
  });
  
  // Применяем стили к сообщениям Django
  document.querySelectorAll('.messages .alert, .messages li').forEach(message => {
    message.classList.add('django-message');
  });
}

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
  // Инициализируем тему
  initTheme();
  
  // Улучшаем формы Django
  enhanceDjangoForms();
  
  // Анимируем карточки при загрузке
  document.querySelectorAll('.card').forEach((card, index) => {
    setTimeout(() => animateElement(card), index * 100);
  });
});

// Экспортируем функции для глобального использования
window.MaroAI = {
  cn,
  getButtonClasses,
  getBadgeClasses,
  createCard,
  createAlert,
  toggleTheme,
  initTheme,
  animateElement,
  showToast,
  enhanceDjangoForms
}; 