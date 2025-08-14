# users/management/commands/import_users.py

import csv
from django.core.management.base import BaseCommand, CommandError
from users.models import User  # 确保从你的 users app 导入 User 模型

class Command(BaseCommand):
    help = 'Imports users from a specified CSV file.'

    def add_arguments(self, parser):
        # 定义一个命令行参数，用于接收 CSV 文件的路径
        parser.add_argument('csv_file_path', type=str, help='The full path to the CSV file to import.')

    def handle(self, *args, **options):
        file_path = options['csv_file_path']

        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                users_created_count = 0
                for row in reader:
                    # 使用 get_or_create 避免重复创建用户
                    # 它会尝试获取一个用户，如果不存在，则创建它
                    user, created = User.objects.get_or_create(
                        username=row['username'],
                        defaults={
                            'email': row['email'],
                            'first_name': row['first_name'],
                            'last_name': row['last_name'],
                            'role': row['role'],
                            # 注意：我们使用 set_password 来正确地哈希密码
                            # 'password': row['password'] 这样做是错误的！
                        }
                    )
                    
                    if created:
                        user.set_password(row['password']) # 对新创建的用户设置密码
                        user.save()
                        users_created_count += 1
                        self.stdout.write(self.style.SUCCESS(f'Successfully created user: {user.username}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'User {user.username} already exists. Skipping.'))

        except FileNotFoundError:
            raise CommandError(f'File not found at: {file_path}')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

        self.stdout.write(self.style.SUCCESS(f'Finished importing. Total new users created: {users_created_count}'))