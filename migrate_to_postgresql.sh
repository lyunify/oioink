#!/bin/bash

# PostgreSQL Migration Script
# Usage: bash migrate_to_postgresql.sh

set -e  # Exit on error

echo "=========================================="
echo "PostgreSQL Data Migration Script"
echo "=========================================="
echo ""

# Color definitions
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Enter project directory
cd "$(dirname "$0")/src"

# 1. Check virtual environment
echo -e "${YELLOW}Step 1: Checking virtual environment...${NC}"
if [ ! -f "../bin/activate" ]; then
    echo -e "${RED}Error: Virtual environment not found${NC}"
    exit 1
fi
source ../bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"
echo ""

# 2. Check and install psycopg2
echo -e "${YELLOW}Step 2: Checking psycopg2...${NC}"
if ! python -c "import psycopg2" 2>/dev/null; then
    echo "Installing psycopg2-binary..."
    pip install psycopg2-binary
    echo -e "${GREEN}✓ psycopg2 installed${NC}"
else
    echo -e "${GREEN}✓ psycopg2 already installed${NC}"
fi
echo ""

# 3. Backup SQLite database
echo -e "${YELLOW}Step 3: Backing up SQLite database...${NC}"
if [ -f "db.sqlite3" ]; then
    BACKUP_FILE="db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)"
    cp db.sqlite3 "$BACKUP_FILE"
    echo -e "${GREEN}✓ Backup created: $BACKUP_FILE${NC}"
    echo "  File size: $(du -h "$BACKUP_FILE" | cut -f1)"
else
    echo -e "${YELLOW}⚠ SQLite database file does not exist, skipping backup${NC}"
fi
echo ""

# 4. Check PostgreSQL connection
echo -e "${YELLOW}Step 4: Checking PostgreSQL connection...${NC}"
if ! python -c "
import os
import sys
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT version();')
print('✓ PostgreSQL connection successful')
print('  Version:', cursor.fetchone()[0][:50])
" 2>&1; then
    echo -e "${RED}✗ PostgreSQL connection failed${NC}"
    echo ""
    echo "Please check:"
    echo "1. Is PostgreSQL service running: brew services start postgresql@15"
    echo "2. Is the database created"
    echo "3. Are database settings in .env file correct"
    exit 1
fi
echo ""

# 5. Create table structure
echo -e "${YELLOW}Step 5: Creating database table structure...${NC}"
python manage.py migrate --noinput
echo -e "${GREEN}✓ Table structure created${NC}"
echo ""

# 6. Export SQLite data
echo -e "${YELLOW}Step 6: Exporting SQLite data...${NC}"
DUMP_FILE="data_dump_$(date +%Y%m%d_%H%M%S).json"

# Temporarily switch to SQLite to export data
python -c "
import os
import sys
import django
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Temporarily change to SQLite
import mysite.settings as settings_module
settings_module.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': 'db.sqlite3',
}

django.setup()
from django.core.management import call_command
with open('$DUMP_FILE', 'w') as f:
    call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], 
                 indent=2, stdout=f, verbosity=0)
print('✓ Data exported: $DUMP_FILE')
"

if [ -f "$DUMP_FILE" ]; then
    FILE_SIZE=$(du -h "$DUMP_FILE" | cut -f1)
    echo -e "${GREEN}✓ Export file size: $FILE_SIZE${NC}"
else
    echo -e "${RED}✗ Export failed${NC}"
    exit 1
fi
echo ""

# 7. Import data to PostgreSQL
echo -e "${YELLOW}Step 7: Importing data to PostgreSQL...${NC}"
python manage.py loaddata "$DUMP_FILE"
echo -e "${GREEN}✓ Data import completed${NC}"
echo ""

# 8. Verify migration
echo -e "${YELLOW}Step 8: Verifying migration results...${NC}"
python -c "
import os
import sys
import django
sys.path.insert(0, '.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.apps import apps

models_to_check = [
    ('accounts', 'Account'),
    ('lessons', 'Lesson'),
    ('tracking', 'Transaction'),
    ('wallet', 'Wallet'),
]

print('Data statistics:')
for app_label, model_name in models_to_check:
    try:
        model = apps.get_model(app_label, model_name)
        count = model.objects.count()
        print(f'  {app_label}.{model_name}: {count} records')
    except Exception as e:
        print(f'  ⚠ {app_label}.{model_name}: Cannot check ({e})')
"
echo ""

echo "=========================================="
echo -e "${GREEN}✓ Migration completed!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Test application: python manage.py runserver"
echo "2. Verify data integrity"
echo "3. If everything is normal, you can delete backup files"
echo ""

