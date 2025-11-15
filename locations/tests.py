from django.test import TestCase
from locations.models import Location


class LocationModelTest(TestCase):
    def setUp(self):
        self.location = Location.objects.create(
            building_name='Science Building',
            building_code='SCI',
            description='Main science building'
        )

    def test_location_creation(self):
        self.assertEqual(self.location.building_name, 'Science Building')
        self.assertEqual(self.location.building_code, 'SCI')

    def test_location_string_representation(self):
        self.assertEqual(str(self.location), 'Science Building (SCI)')
