#!/bin/bash
cd /Users/katy/project/eduaify/src
source ../bin/activate

echo "Checking database connection..."
python -c "
import os
import sys
import django
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connection

engine = connection.settings_dict['ENGINE']
db_name = connection.settings_dict['NAME']
db_user = connection.settings_dict['USER']

print('=' * 60)
if 'postgresql' in engine:
    print('✅ Connected to PostgreSQL')
    print(f'   Database: {db_name}')
    print(f'   User: {db_user}')
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f'   Version: {version[:60]}...')
        print('✅ Connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
elif 'sqlite' in engine:
    print('❌ Connected to SQLite')
    print(f'   Database file: {db_name}')
else:
    print(f'⚠️  Unknown database engine: {engine}')
print('=' * 60)
"

