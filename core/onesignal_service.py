import requests
import json
from django.conf import settings
from accounts.models import User

class OneSignalService:
    """Сервис для отправки push-уведомлений через OneSignal"""
    
    # OneSignal App ID (получен от пользователя)
    APP_ID = "24c6c8e0-f55e-45a6-bca6-3985329161c7"
    
    # OneSignal REST API URL
    API_URL = "https://onesignal.com/api/v1/notifications"
    
    @classmethod
    def send_notification_to_users(cls, title, message, user_ids=None, target_roles=None, is_urgent=False):
        """
        Отправляет push-уведомление пользователям через OneSignal
        
        Args:
            title (str): Заголовок уведомления
            message (str): Текст уведомления
            user_ids (list): Список ID пользователей (опционально)
            target_roles (list): Список ролей пользователей (опционально)
            is_urgent (bool): Срочное уведомление
        """
        try:
            print(f"🔔 OneSignalService: Отправляем уведомление - {title}")
            
            # Определяем получателей
            if user_ids:
                # Отправляем конкретным пользователям по ID
                player_ids = cls._get_player_ids_by_user_ids(user_ids)
            elif target_roles:
                # Отправляем пользователям с определенными ролями
                player_ids = cls._get_player_ids_by_roles(target_roles)
            else:
                # Отправляем всем пользователям
                player_ids = cls._get_all_player_ids()
            
            if not player_ids:
                print("🔔 OneSignalService: Нет активных Player ID для отправки")
                return False
            
            # Подготавливаем данные для OneSignal
            notification_data = {
                "app_id": cls.APP_ID,
                "include_player_ids": player_ids,
                "headings": {"en": title, "ru": title},
                "contents": {"en": message, "ru": message},
                "priority": 10 if is_urgent else 5,  # Высокий приоритет для срочных
                "ttl": 86400,  # Время жизни уведомления (24 часа)
                "sound": "default",  # Звук по умолчанию
                "badge": {"+1": True},  # Увеличиваем badge
                "data": {
                    "type": "broadcast",
                    "is_urgent": is_urgent,
                    "title": title,
                    "message": message
                }
            }
            
            # Отправляем уведомление
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "Authorization": "Basic YOUR_ONESIGNAL_REST_API_KEY"  # Нужно будет заменить
            }
            
            print(f"🔔 OneSignalService: Отправляем {len(player_ids)} уведомлений")
            
            # Временно отключаем реальную отправку для тестирования
            # response = requests.post(cls.API_URL, headers=headers, data=json.dumps(notification_data))
            
            # Логируем что бы отправили
            print(f"🔔 OneSignalService: Данные для отправки: {json.dumps(notification_data, indent=2, ensure_ascii=False)}")
            print(f"🔔 OneSignalService: Player IDs: {player_ids}")
            
            # Имитируем успешную отправку
            print("🔔 OneSignalService: Уведомления отправлены успешно (тестовый режим)")
            return True
            
        except Exception as e:
            print(f"🔔 OneSignalService: Ошибка отправки уведомления - {e}")
            return False
    
    @classmethod
    def _get_player_ids_by_user_ids(cls, user_ids):
        """Получает Player ID для конкретных пользователей"""
        try:
            print(f"🔔 OneSignalService: Получаем Player ID для пользователей: {user_ids}")
            
            users = User.objects.filter(id__in=user_ids).exclude(onesignal_player_id__isnull=True).exclude(onesignal_player_id__exact='')
            player_ids = [user.onesignal_player_id for user in users if user.onesignal_player_id]
            
            print(f"🔔 OneSignalService: Найдено Player ID: {player_ids}")
            return player_ids
        except Exception as e:
            print(f"🔔 OneSignalService: Ошибка получения Player ID - {e}")
            return []
    
    @classmethod
    def _get_player_ids_by_roles(cls, roles):
        """Получает Player ID для пользователей с определенными ролями"""
        try:
            print(f"🔔 OneSignalService: Получаем Player ID для ролей: {roles}")
            
            # Получаем пользователей с указанными ролями, у которых есть Player ID
            users = User.objects.filter(
                role__in=roles
            ).exclude(
                onesignal_player_id__isnull=True
            ).exclude(
                onesignal_player_id__exact=''
            )
            
            print(f"🔔 OneSignalService: Найдено пользователей с Player ID: {users.count()}")
            
            player_ids = [user.onesignal_player_id for user in users if user.onesignal_player_id]
            print(f"🔔 OneSignalService: Player ID для ролей {roles}: {player_ids}")
            
            return player_ids
        except Exception as e:
            print(f"🔔 OneSignalService: Ошибка получения Player ID по ролям - {e}")
            return []
    
    @classmethod
    def _get_all_player_ids(cls):
        """Получает Player ID всех активных пользователей"""
        try:
            print("🔔 OneSignalService: Получаем Player ID всех пользователей")
            
            # Получаем всех пользователей с Player ID
            users = User.objects.exclude(
                onesignal_player_id__isnull=True
            ).exclude(
                onesignal_player_id__exact=''
            )
            
            player_ids = [user.onesignal_player_id for user in users if user.onesignal_player_id]
            print(f"🔔 OneSignalService: Всего Player ID: {len(player_ids)}")
            
            return player_ids
        except Exception as e:
            print(f"🔔 OneSignalService: Ошибка получения всех Player ID - {e}")
            return []
    
    @classmethod
    def save_player_id(cls, user_id, player_id):
        """
        Сохраняет Player ID для пользователя в базе данных
        
        Args:
            user_id (int): ID пользователя
            player_id (str): OneSignal Player ID
        """
        try:
            user = User.objects.get(id=user_id)
            user.onesignal_player_id = player_id
            user.save()
            print(f"🔔 OneSignalService: Player ID сохранен для пользователя {user.username}: {player_id}")
            return True
        except User.DoesNotExist:
            print(f"🔔 OneSignalService: Пользователь с ID {user_id} не найден")
            return False
        except Exception as e:
            print(f"🔔 OneSignalService: Ошибка сохранения Player ID - {e}")
            return False
