from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()

class PhoneBackend(ModelBackend):
    """
    Универсальный бэкенд аутентификации, поддерживающий:
    - Аутентификацию по номеру телефона
    - Аутентификацию по username
    - Аутентификацию по email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
            
        # Пытаемся найти пользователя по различным полям
        user = None
        
        # 1. Сначала пытаемся найти по номеру телефона
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
            
        # 2. Затем пытаемся найти по username
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
            
        # 3. Наконец, пытаемся найти по email
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
            
        # Если ничего не найдено, возвращаем None
        return None 