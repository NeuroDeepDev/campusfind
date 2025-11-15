from django.test import TestCase
from django.contrib.auth.hashers import make_password
from users.models import Student, Admin


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            email='test@university.edu',
            password_hash=make_password('testpass123'),
            first_name='Test',
            last_name='Student',
            student_id='STU123',
            phone='555-0001'
        )

    def test_student_creation(self):
        self.assertEqual(self.student.email, 'test@university.edu')
        self.assertEqual(self.student.student_id, 'STU123')
        self.assertFalse(self.student.is_verified)

    def test_student_string_representation(self):
        expected = 'Test Student (test@university.edu)'
        self.assertEqual(str(self.student), expected)


class AdminModelTest(TestCase):
    def setUp(self):
        self.admin = Admin.objects.create(
            email='admin@university.edu',
            password_hash=make_password('adminpass123'),
            first_name='Admin',
            last_name='User'
        )

    def test_admin_creation(self):
        self.assertEqual(self.admin.email, 'admin@university.edu')
        self.assertTrue(self.admin.is_staff)

    def test_admin_string_representation(self):
        expected = 'Admin User (admin@university.edu)'
        self.assertEqual(str(self.admin), expected)
