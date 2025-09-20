#!/bin/bash
echo "🤖 Установка автоматического GPS мониторинга"
echo "=============================================="

echo "📦 Установка Python пакетов..."
pip install -r requirements_gps.txt

echo "🔧 Установка Chrome драйвера..."
pip install webdriver-manager

echo "✅ Установка завершена!"
echo ""
echo "🚀 Для запуска мониторинга:"
echo "   python selenium_gps_monitor.py"
