from django.core.management.base import BaseCommand
from django.db import connection
from pathlib import Path


class Command(BaseCommand):
    help = 'Load sample data from SQL file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='sql/campusfind_schema_and_seed.sql',
            help='Path to SQL file to load'
        )

    def handle(self, *args, **options):
        sql_file = Path(options['file'])
        
        if not sql_file.exists():
            self.stdout.write(
                self.style.ERROR(f'SQL file not found: {sql_file}')
            )
            return

        try:
            with open(sql_file, 'r') as f:
                sql = f.read()

            # Split SQL into individual statements
            statements = [s.strip() for s in sql.split(';') if s.strip() and not s.strip().startswith('--')]

            with connection.cursor() as cursor:
                for statement in statements:
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        # Ignore errors for CREATE IF NOT EXISTS and INSERT OR IGNORE
                        if 'already exists' not in str(e) and 'UNIQUE constraint failed' not in str(e):
                            self.stdout.write(self.style.WARNING(f'Error executing statement: {str(e)[:100]}'))

            self.stdout.write(
                self.style.SUCCESS('Sample data loaded successfully')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading sample data: {str(e)}')
            )
