# venues/management/commands/import_venues.py

import csv
from django.core.management.base import BaseCommand, CommandError
from venues.models import Venue  # 从 venues app 导入 Venue 模型

class Command(BaseCommand):
    help = 'Imports venues from a specified CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The full path to the CSV file to import.')

    def handle(self, *args, **options):
        file_path = options['csv_file_path']

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                venues_created_count = 0
                for row in reader:
                    # 对于布尔值，需要将 CSV 中的字符串 'True'/'False' 转换为 Python 的布尔值
                    has_projector_bool = row['has_projector'].lower() == 'true'
                    has_whiteboard_bool = row['has_whiteboard'].lower() == 'true'

                    venue, created = Venue.objects.get_or_create(
                        name=row['name'],
                        defaults={
                            'capacity': int(row['capacity']), # 容量通常是整数，需要转换
                            'location': row['location'],
                            'has_projector': has_projector_bool,
                            'has_whiteboard': has_whiteboard_bool,
                        }
                    )
                    
                    if created:
                        venues_created_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Successfully created venue: {venue.name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Venue "{venue.name}" already exists. Skipping.'))

        except FileNotFoundError:
            raise CommandError(f'File not found at: {file_path}')
        except ValueError:
             raise CommandError(f'Invalid data found in CSV. Ensure "capacity" is a number.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

        self.stdout.write(self.style.SUCCESS(f'Finished importing. Total new venues created: {venues_created_count}'))
