#!/bin/sh
set -e

echo "🚀 Starting Celery Worker..."
echo "📍 Working directory: $(pwd)"
echo "📁 Files in directory:"
ls -la | head -n 20

exec celery -A celery_app worker --loglevel=info
