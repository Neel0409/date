import datetime
from django.test import TestCase, Client
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import DateSelection
from .forms import DateSelectionForm


class DateSimulatorTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.today = timezone.localdate() if hasattr(timezone, 'localdate') else timezone.now().date()
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.yesterday = self.today - datetime.timedelta(days=1)

    def test_home_page_renders_properly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('When should we go on our date?', content)
        self.assertIn('Something special (I&#x27;ll cook for you ❤️)', content)
        self.assertIn('Other (Let me decide)', content)
        self.assertIn('Other (Your own idea)', content)

    def test_past_date_rejected(self):
        form_data = {
            'name': 'Test Past',
            'selected_date': self.yesterday.strftime('%Y-%m-%d'),
            'date_choice': 'Beach Date',
            'food_choice': 'Pizza',
            'activity_choice': 'Long Drive',
            'consent': 'on'
        }
        form = DateSelectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('selected_date', form.errors)
        self.assertIn('Please choose today or a future date for our date!', form.errors['selected_date'][0])

        response = self.client.post('/', form_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Please choose today or a future date for our date!', response.content.decode('utf-8'))

    def test_other_without_custom_text_rejected(self):
        form_data = {
            'name': 'Test Other Empty',
            'selected_date': self.tomorrow.strftime('%Y-%m-%d'),
            'date_choice': 'Other',
            'custom_date_choice': '',
            'food_choice': 'Other',
            'custom_food_choice': '   ',
            'activity_choice': 'Other',
            'custom_activity_choice': '',
            'consent': 'on'
        }
        form = DateSelectionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('custom_date_choice', form.errors)
        self.assertIn('custom_food_choice', form.errors)
        self.assertIn('custom_activity_choice', form.errors)

    def test_valid_standard_submission(self):
        form_data = {
            'name': 'Kavya',
            'selected_date': self.tomorrow.strftime('%Y-%m-%d'),
            'date_choice': 'Candlelight Dinner',
            'food_choice': "Something special (I'll cook for you ❤️)",
            'activity_choice': 'Dancing',
            'message': 'Excited for this date!',
            'consent': 'on'
        }
        response = self.client.post('/', form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/success/')

        saved = DateSelection.objects.filter(name='Kavya').first()
        self.assertIsNotNone(saved)
        self.assertEqual(saved.selected_date, self.tomorrow)
        self.assertEqual(saved.food_choice, "Something special (I'll cook for you ❤️)")
        self.assertEqual(saved.activity_choice, 'Dancing')
        self.assertEqual(saved.custom_date_choice, '')

    def test_valid_custom_other_submission(self):
        form_data = {
            'name': 'Aanya',
            'selected_date': (self.today + datetime.timedelta(days=5)).strftime('%Y-%m-%d'),
            'date_choice': 'Other',
            'custom_date_choice': 'Rooftop Cafe under the stars',
            'food_choice': 'Other',
            'custom_food_choice': 'Handmade Sushi and Wine',
            'activity_choice': 'Other',
            'custom_activity_choice': 'Acoustic guitar by the bonfire',
            'message': 'Can not wait!',
            'consent': 'on'
        }
        response = self.client.post('/', form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/success/')

        saved = DateSelection.objects.filter(name='Aanya').first()
        self.assertIsNotNone(saved)
        self.assertEqual(saved.date_choice, 'Other')
        self.assertEqual(saved.custom_date_choice, 'Rooftop Cafe under the stars')
        self.assertEqual(saved.food_choice, 'Other')
        self.assertEqual(saved.custom_food_choice, 'Handmade Sushi and Wine')
        self.assertEqual(saved.activity_choice, 'Other')
        self.assertEqual(saved.custom_activity_choice, 'Acoustic guitar by the bonfire')

    def test_admin_dashboard_integration(self):
        User = get_user_model()
        User.objects.create_superuser('admin_test', 'admin_test@test.com', 'adminpass123')
        self.client.login(username='admin_test', password='adminpass123')

        item = DateSelection.objects.create(
            name='Simran',
            selected_date=self.tomorrow,
            date_choice='Other',
            custom_date_choice='Private Yacht',
            food_choice='Other',
            custom_food_choice='Italian Truffle Pizza',
            activity_choice='Other',
            custom_activity_choice='Midnight Cruise',
            message='Counting the hours!',
            consent=True
        )

        response = self.client.get('/admin/simulator/dateselection/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Simran', content)
        self.assertIn('Other: Private Yacht', content)
        self.assertIn('Other: Italian Truffle Pizza', content)
        self.assertIn('Other: Midnight Cruise', content)
