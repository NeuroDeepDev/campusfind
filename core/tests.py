from django.test import TestCase

from .forms import ReportForm


class ReportFormCategoryTests(TestCase):
    def test_category_field_has_standardized_options_and_placeholder(self):
        form = ReportForm()

        self.assertEqual(form.fields['category'].choices[0], ('', 'Select any'))
        self.assertEqual(
            [value for value, _ in form.fields['category'].choices if value],
            [
                'Electronics',
                'Documents',
                'Jewelry & Valuables',
                'Stationery & Books',
                'Personal Belongings',
                'Others',
            ],
        )

        rendered = form.fields['category'].widget.render('category', '')
        self.assertIn('value=""', rendered)
        self.assertIn('disabled', rendered)

    def test_blank_category_is_rejected(self):
        form = ReportForm(
            data={
                'item_name': 'Phone',
                'category': '',
                'report_type': 'LOST',
                'description': 'A test description',
                'location': 'Library',
                'date_lost_found': '2024-01-01',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
