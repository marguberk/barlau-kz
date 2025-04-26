try:
    # Существующий код...
    
    # Добавляем проверку на ошибки при конвертации UUID
    from django.db import connection
    
    def get_valid_notifications(user):
        """Получает только уведомления с валидным UUID"""
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM core_notification 
            WHERE recipient_id = %s 
            AND LENGTH(id) = 36
            AND id ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        """, [user.id])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Замена нормального запроса на проверенный запрос
    # Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    # заменяем на наш безопасный метод
    
except Exception as e:
    # В случае ошибки импорта или другой проблемы, просто продолжаем работу
    pass 