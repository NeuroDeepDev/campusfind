from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Student, Admin
from categories.models import Category
from locations.models import Location


class Command(BaseCommand):
    help = 'Load sample data for testing'

    def handle(self, *args, **options):
        # Create sample users/students
        students_data = [
            {'username': 'alice', 'email': 'alice@university.edu', 'first_name': 'Alice', 'last_name': 'Johnson', 'student_id': 'STU001'},
            {'username': 'bob', 'email': 'bob@university.edu', 'first_name': 'Bob', 'last_name': 'Smith', 'student_id': 'STU002'},
            {'username': 'charlie', 'email': 'charlie@university.edu', 'first_name': 'Charlie', 'last_name': 'Brown', 'student_id': 'STU003'},
            {'username': 'diana', 'email': 'diana@university.edu', 'first_name': 'Diana', 'last_name': 'Prince', 'student_id': 'STU004'},
            {'username': 'eve', 'email': 'eve@university.edu', 'first_name': 'Eve', 'last_name': 'Wilson', 'student_id': 'STU005'},
        ]

        for student_info in students_data:
            user, created = User.objects.get_or_create(
                username=student_info['username'],
                defaults={
                    'email': student_info['email'],
                    'first_name': student_info['first_name'],
                    'last_name': student_info['last_name'],
                }
            )
            if created:
                user.set_password('TestPass123!')
                user.save()
                Student.objects.create(
                    user=user,
                    student_id=student_info['student_id'],
                    phone='+1-555-0100',
                    is_verified=True
                )

        # Create admin users
        admins_data = [
            {'username': 'admin', 'email': 'admin@university.edu', 'first_name': 'Admin', 'last_name': 'User'},
            {'username': 'staff', 'email': 'staff@university.edu', 'first_name': 'Staff', 'last_name': 'Member'},
        ]

        for admin_info in admins_data:
            user, created = User.objects.get_or_create(
                username=admin_info['username'],
                defaults={
                    'email': admin_info['email'],
                    'first_name': admin_info['first_name'],
                    'last_name': admin_info['last_name'],
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                user.set_password('TestPass123!')
                user.save()
                Admin.objects.create(user=user, is_verified=True)

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Phones, laptops, chargers'},
            {'name': 'Accessories', 'description': 'Keys, wallets, bags'},
            {'name': 'Clothing', 'description': 'Jackets, hats, scarves'},
            {'name': 'Books', 'description': 'Textbooks, notebooks'},
            {'name': 'Other', 'description': 'Miscellaneous items'},
        ]

        for cat in categories_data:
            Category.objects.get_or_create(name=cat['name'], defaults={'description': cat['description']})

        # Create locations
        locations_data = [
            {'building_name': 'Library', 'building_code': 'LIB', 'description': 'Main Library Building'},
            {'building_name': 'Student Center', 'building_code': 'SC', 'description': 'Student Activity Center'},
            {'building_name': 'Cafeteria', 'building_code': 'CAF', 'description': 'Main Cafeteria'},
            {'building_name': 'Gym', 'building_code': 'GYM', 'description': 'Athletic Center'},
            {'building_name': 'Parking Lot', 'building_code': 'PKG', 'description': 'North Parking Lot'},
        ]

        for loc in locations_data:
            Location.objects.get_or_create(building_name=loc['building_name'], defaults={'building_code': loc['building_code'], 'description': loc['description']})

        self.stdout.write(
            self.style.SUCCESS('Sample data loaded successfully')
        )
