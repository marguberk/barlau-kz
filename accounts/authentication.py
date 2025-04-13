from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class PhoneBackend(ModelBackend):
    """
    Аутентификация пользователя по номеру телефона вместо имени пользователя.
    Также поддерживает стандартную аутентификацию по username как резервный метод.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
            
        # Пытаемся найти пользователя по номеру телефона
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Если пользователь не найден по телефону, возвращаем None
            pass
            
        # Если не найден по телефону, используем стандартный бэкенд
        return super().authenticate(request, username=username, password=password, **kwargs) 