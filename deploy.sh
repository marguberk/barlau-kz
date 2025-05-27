#!/bin/bash

# Deploy script for Barlau.kz on Plesk hosting
# This script should be run on the server after git pull

echo "🚀 Starting deployment for Barlau.kz..."

# Set environment variables
export DJANGO_SETTINGS_MODULE=barlau.settings_production

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create cache table
echo "💾 Creating cache table..."
python manage.py createcachetable

# Restart application (Plesk specific)
echo "🔄 Restarting application..."
touch /var/www/vhosts/barlau.org/httpdocs/restart.txt

echo "✅ Deployment completed successfully!"
echo "🌐 Your site should be available at: https://barlau.org" 