#!/bin/bash

# Скрипт для получения SHA-256 отпечатка сертификата для Android TWA
# Используется для настройки Digital Asset Links в assetlinks.json

# Убедитесь, что переменные окружения ANDROID_HOME установлены 
# и keytool доступен в PATH

# Путь к keystore файлу (обычно app/release-key.keystore)
KEYSTORE_PATH="twa-build/app/release-key.keystore"

# Пароль для keystore (тот же, что используется при создании)
KEYSTORE_PASSWORD="password"

# Алиас ключа
KEY_ALIAS="key"

# Получение SHA-256 отпечатка
echo "Получение SHA-256 отпечатка сертификата из $KEYSTORE_PATH..."

if [ -f "$KEYSTORE_PATH" ]; then
    # Выполняем команду keytool для получения информации о сертификате
    keytool -list -v -keystore "$KEYSTORE_PATH" -alias "$KEY_ALIAS" -storepass "$KEYSTORE_PASSWORD" | grep "SHA256" | awk '{print $2}'
    
    echo ""
    echo "Скопируйте этот отпечаток в файл .well-known/assetlinks.json на вашем веб-сервере"
    echo "И в файл twa-build/assetlinks.json в проекте"
else
    echo "Ошибка: Файл keystore не найден по пути $KEYSTORE_PATH"
    echo "Убедитесь, что вы создали keystore для подписи приложения"
    echo ""
    echo "Для создания keystore используйте команду:"
    echo "keytool -genkey -v -keystore $KEYSTORE_PATH -alias $KEY_ALIAS -keyalg RSA -keysize 2048 -validity 10000 -storepass $KEYSTORE_PASSWORD"
fi 