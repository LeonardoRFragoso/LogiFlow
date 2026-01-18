#!/bin/sh
set -e

echo "⏰ Starting Celery Beat..."
echo "📍 Working directory: $(pwd)"
echo "📁 Files in directory:"
ls -la | head -n 20

exec celery -A celery_app beat --loglevel=info
