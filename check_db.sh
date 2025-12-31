#!/bin/bash
cd /Users/katy/project/eduaify/src
source ../bin/activate

echo "检查数据库连接..."
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
    print('✅ 连接的是 PostgreSQL')
    print(f'   数据库: {db_name}')
    print(f'   用户: {db_user}')
    
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f'   版本: {version[:60]}...')
        print('✅ 连接成功！')
    except Exception as e:
        print(f'❌ 连接失败: {e}')
elif 'sqlite' in engine:
    print('❌ 连接的是 SQLite')
    print(f'   数据库文件: {db_name}')
else:
    print(f'⚠️  未知的数据库引擎: {engine}')
print('=' * 60)
"

