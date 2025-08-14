# equipment/management/commands/import_equipment.py

import csv
import datetime
from django.core.management.base import BaseCommand, CommandError
from equipment.models import Equipment, EquipmentCategory

class Command(BaseCommand):
    help = 'Imports equipment items from a specified CSV file. Creates categories if they do not exist.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='The full path to the CSV file to import.')

    def handle(self, *args, **options):
        file_path = options['csv_file_path']

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                items_processed_count = 0
                for row in reader:
                    # 1. Get or Create EquipmentCategory
                    category_name = row.get('category_name')
                    equipment_category = None
                    if category_name:
                        try:
                            # get_or_create will create the category if it doesn't exist
                            equipment_category, created_cat = EquipmentCategory.objects.get_or_create(name=category_name)
                            if created_cat:
                                self.stdout.write(self.style.NOTICE(f'Created new EquipmentCategory: {category_name}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Error getting/creating category {category_name}: {e}. Skipping equipment {row.get("name")}.'))
                            continue
                    
                    # 2. Parse Purchase Date
                    purchase_date = None
                    purchase_date_str = row.get('purchase_date')
                    if purchase_date_str:
                        try:
                            purchase_date = datetime.datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            self.stdout.write(self.style.ERROR(f'Invalid purchase_date format for {row.get("name")}: {purchase_date_str}. Skipping purchase date.'))
                            
                    # 3. Ensure quantity fields are integers
                    try:
                        quantity_total = int(row.get('quantity_total', 1))
                        quantity_available = int(row.get('quantity_available', 1))
                    except ValueError:
                        self.stdout.write(self.style.ERROR(f'Invalid quantity_total or quantity_available for {row.get("name")}. Skipping row.'))
                        continue

                    # 4. Use identifier as the primary unique field for equipment
                    identifier = row.get('identifier')
                    if not identifier:
                        self.stdout.write(self.style.ERROR(f'Identifier missing for equipment {row.get("name")}. Skipping row.'))
                        continue

                    # 5. Create or Get Equipment
                    item, created = Equipment.objects.get_or_create(
                        identifier=identifier, # Use identifier for get_or_create
                        defaults={
                            'name': row.get('name', 'Unnamed Equipment'),
                            'category': equipment_category,
                            'description': row.get('description', ''),
                            'quantity_total': quantity_total,
                            'quantity_available': quantity_available,
                            'status': row.get('status', Equipment.STATUS_AVAILABLE), # Default to available if not provided
                            'purchase_date': purchase_date,
                        }
                    )
                    
                    if created:
                        items_processed_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Successfully created equipment: {item.name} ({item.identifier})'))
                    else:
                        # Optional: update existing item if fields are different
                        # item.name = row.get('name', item.name)
                        # item.category = equipment_category # Update category if it changed
                        # ... other fields
                        # item.save()
                        self.stdout.write(self.style.WARNING(f'Equipment "{item.name}" with identifier "{item.identifier}" already exists.'))

        except FileNotFoundError:
            raise CommandError(f'File not found at: {file_path}')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

        self.stdout.write(self.style.SUCCESS(f'Finished importing. Total new equipment items created: {items_processed_count}'))

