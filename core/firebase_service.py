import firebase_admin
from firebase_admin import credentials, messaging
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class FirebaseService:
    """Сервис для отправки push уведомлений через Firebase"""
    
    _app = None
    
    @classmethod
    def initialize(cls):
        """Инициализация Firebase Admin SDK"""
        try:
            if cls._app is None:
                # Путь к файлу с ключами Firebase
                cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
                
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    cls._app = firebase_admin.initialize_app(cred)
                    logger.info("Firebase Admin SDK инициализирован успешно")
                else:
                    logger.warning("Файл Firebase credentials не найден, push уведомления отключены")
                    return False
            return True
        except Exception as e:
            logger.error(f"Ошибка инициализации Firebase: {e}")
            return False
    
    @classmethod
    def send_notification(cls, fcm_token, title, body, data=None):
        """Отправить уведомление на конкретное устройство"""
        try:
            if not cls.initialize():
                return False
            
            # Создаем сообщение
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=fcm_token,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='notification',
                        channel_id='barlau_notifications',
                        priority='high',
                        default_sound=True,
                        default_vibrate_timings=True
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            alert=messaging.ApsAlert(
                                title=title,
                                body=body
                            ),
                            sound='default',
                            badge=1,
                            content_available=True
                        )
                    )
                )
            )
            
            # Отправляем сообщение
            response = messaging.send(message)
            logger.info(f"Уведомление отправлено успешно: {response}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка отправки Firebase уведомления: {e}")
            return False
    
    @classmethod
    def send_multicast_notification(cls, fcm_tokens, title, body, data=None):
        """Отправить уведомление на несколько устройств"""
        try:
            if not cls.initialize():
                return False
            
            if not fcm_tokens:
                logger.warning("Список FCM токенов пуст")
                return False
            
            # Создаем сообщение для мультикаста
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                tokens=fcm_tokens,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='notification',
                        channel_id='barlau_notifications',
                        priority='high',
                        default_sound=True,
                        default_vibrate_timings=True
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            alert=messaging.ApsAlert(
                                title=title,
                                body=body
                            ),
                            sound='default',
                            badge=1,
                            content_available=True
                        )
                    )
                )
            )
            
            # Отправляем мультикаст сообщение
            response = messaging.send_multicast(message)
            logger.info(f"Мультикаст уведомление отправлено: успешно {response.success_count}, ошибок {response.failure_count}")
            
            # Логируем ошибки если есть
            if response.failure_count > 0:
                for idx, resp in enumerate(response.responses):
                    if not resp.success:
                        logger.error(f"Ошибка отправки на токен {idx}: {resp.exception}")
            
            return response.success_count > 0
            
        except Exception as e:
            logger.error(f"Ошибка отправки Firebase мультикаст уведомления: {e}")
            return False
