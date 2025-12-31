"""
Django management command: Migrate data from SQLite to PostgreSQL

Usage:
    python manage.py migrate_to_postgresql

This command will:
1. Check PostgreSQL connection
2. Backup current SQLite data
3. Create table structure in PostgreSQL
4. Export SQLite data
5. Import data to PostgreSQL
6. Verify migration results
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import os
import json
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = 'Migrate data from SQLite to PostgreSQL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-backup',
            action='store_true',
            help='Skip SQLite backup step',
        )
        parser.add_argument(
            '--skip-verify',
            action='store_true',
            help='Skip data verification step',
        )
        parser.add_argument(
            '--dump-file',
            type=str,
            default=None,
            help='Specify data export file path (default: data_dump_YYYYMMDD_HHMMSS.json)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('PostgreSQL Data Migration Tool'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')

        # 1. Check current database configuration
        if not self.check_database_config():
            return

        # 2. Backup SQLite data
        if not options['skip_backup']:
            if not self.backup_sqlite():
                return

        # 3. Check PostgreSQL connection
        if not self.check_postgresql_connection():
            return

        # 4. Create table structure
        if not self.create_tables():
            return

        # 5. Export SQLite data
        dump_file = options.get('dump_file') or self.get_dump_filename()
        if not self.export_data(dump_file):
            return

        # 6. Import data to PostgreSQL
        if not self.import_data(dump_file):
            return

        # 7. Verify migration results
        if not options['skip_verify']:
            if not self.verify_migration():
                return

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✅ Migration completed!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write('Next steps:')
        self.stdout.write('1. Test application functionality')
        self.stdout.write('2. Verify data integrity')
        self.stdout.write('3. If everything is normal, you can delete SQLite backup files')

    def check_database_config(self):
        """Check database configuration"""
        self.stdout.write('📋 Step 1: Checking database configuration...')
        
        db_engine = settings.DATABASES['default']['ENGINE']
        
        if 'sqlite' in db_engine:
            self.stdout.write(self.style.WARNING('⚠️  Currently using SQLite'))
            self.stdout.write(self.style.WARNING('   Please update settings.py to configure PostgreSQL first'))
            self.stdout.write('')
            response = input('Continue? This will switch to PostgreSQL configuration (y/N): ')
            if response.lower() != 'y':
                self.stdout.write(self.style.ERROR('❌ Cancelled'))
                return False
        elif 'postgresql' in db_engine:
            self.stdout.write(self.style.SUCCESS('✅ PostgreSQL configured'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Unknown database engine: {db_engine}'))
            return False
        
        self.stdout.write('')
        return True

    def backup_sqlite(self):
        """Backup SQLite database"""
        self.stdout.write('💾 Step 2: Backing up SQLite data...')
        
        sqlite_path = Path(settings.BASE_DIR) / 'db.sqlite3'
        if not sqlite_path.exists():
            self.stdout.write(self.style.WARNING('⚠️  SQLite database file does not exist, skipping backup'))
            return True
        
        backup_path = sqlite_path.with_suffix('.sqlite3.backup')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = sqlite_path.parent / f'db.sqlite3.backup_{timestamp}'
        
        try:
            import shutil
            shutil.copy2(sqlite_path, backup_path)
            self.stdout.write(self.style.SUCCESS(f'✅ Backup created: {backup_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Backup failed: {e}'))
            return False
        
        self.stdout.write('')
        return True

    def check_postgresql_connection(self):
        """Check PostgreSQL connection"""
        self.stdout.write('🔌 Step 3: Checking PostgreSQL connection...')
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS('✅ PostgreSQL connection successful'))
                self.stdout.write(f'   Version: {version[:50]}...')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ PostgreSQL connection failed: {e}'))
            self.stdout.write('')
            self.stdout.write('Please check:')
            self.stdout.write('1. Is PostgreSQL service running')
            self.stdout.write('2. Are database settings correct (.env file)')
            self.stdout.write('3. Have database and user been created')
            return False
        
        self.stdout.write('')
        return True

    def create_tables(self):
        """Create table structure in PostgreSQL"""
        self.stdout.write('🏗️  Step 4: Creating database table structure...')
        
        try:
            call_command('migrate', verbosity=0, interactive=False)
            self.stdout.write(self.style.SUCCESS('✅ Table structure created'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to create table structure: {e}'))
            return False
        
        self.stdout.write('')
        return True

    def export_data(self, dump_file):
        """Export data from SQLite"""
        self.stdout.write('📤 Step 5: Exporting SQLite data...')
        
        # Temporarily switch to SQLite configuration
        original_engine = settings.DATABASES['default']['ENGINE']
        original_name = settings.DATABASES['default']['NAME']
        
        # Switch to SQLite
        settings.DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
        settings.DATABASES['default']['NAME'] = Path(settings.BASE_DIR) / 'db.sqlite3'
        
        try:
            # Reconnect database
            from django.db import connections
            connections['default'].close()
            
            dump_path = Path(settings.BASE_DIR) / dump_file
            with open(dump_path, 'w', encoding='utf-8') as f:
                call_command('dumpdata', 
                           exclude=['auth.permission', 'contenttypes'],
                           indent=2,
                           stdout=f,
                           verbosity=0)
            
            self.stdout.write(self.style.SUCCESS(f'✅ Data exported: {dump_path}'))
            self.stdout.write(f'   File size: {dump_path.stat().st_size / 1024 / 1024:.2f} MB')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to export data: {e}'))
            return False
        finally:
            # Restore PostgreSQL configuration
            settings.DATABASES['default']['ENGINE'] = original_engine
            settings.DATABASES['default']['NAME'] = original_name
            from django.db import connections
            connections['default'].close()
        
        self.stdout.write('')
        return True

    def import_data(self, dump_file):
        """Import data to PostgreSQL"""
        self.stdout.write('📥 Step 6: Importing data to PostgreSQL...')
        
        dump_path = Path(settings.BASE_DIR) / dump_file
        if not dump_path.exists():
            self.stdout.write(self.style.ERROR(f'❌ Export file does not exist: {dump_path}'))
            return False
        
        try:
            call_command('loaddata', dump_file, verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Data import completed'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to import data: {e}'))
            self.stdout.write('')
            self.stdout.write('Common issues:')
            self.stdout.write('1. Data format incompatibility')
            self.stdout.write('2. Foreign key constraint conflicts')
            self.stdout.write('3. Unique constraint conflicts')
            return False
        
        self.stdout.write('')
        return True

    def verify_migration(self):
        """Verify migration results"""
        self.stdout.write('🔍 Step 7: Verifying migration results...')
        
        try:
            # Check data for some key models
            from django.apps import apps
            
            models_to_check = [
                ('accounts', 'Account'),
                ('lessons', 'Lesson'),
                ('tracking', 'Transaction'),
                ('wallet', 'Wallet'),
            ]
            
            all_ok = True
            for app_label, model_name in models_to_check:
                try:
                    model = apps.get_model(app_label, model_name)
                    count = model.objects.count()
                    self.stdout.write(f'   {app_label}.{model_name}: {count} records')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'   ⚠️  {app_label}.{model_name}: Cannot check ({e})'))
                    all_ok = False
            
            if all_ok:
                self.stdout.write(self.style.SUCCESS('✅ Data verification passed'))
            else:
                self.stdout.write(self.style.WARNING('⚠️  Some models cannot be verified, please check manually'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Verification failed: {e}'))
            return False
        
        self.stdout.write('')
        return True

    def get_dump_filename(self):
        """Generate export filename"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'data_dump_{timestamp}.json'

