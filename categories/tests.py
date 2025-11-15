from django.test import TestCase
from categories.models import Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(self.category.description, 'Electronic devices')

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), 'Electronics')
