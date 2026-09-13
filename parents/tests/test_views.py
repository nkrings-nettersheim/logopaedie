import shutil
import tempfile

from django.contrib.auth.models import User, Permission
from django.core import mail
from django.test import TestCase, Client, override_settings
from django.urls import reverse

from parents.models import Parents_sheet
from reports.models import Patient, Document

WIZARD_PREFIX = 'parents_sheet_wizard'


class ParentsSheetWizardTest(TestCase):

    def setUp(self):
        self.url = reverse('parents:parents_sheet_wizard', args=['test-token'])
        self.client = Client()

    def _post_step(self, step, data):
        payload = {f'{WIZARD_PREFIX}-current_step': str(step)}
        for key, value in data.items():
            payload[f'{step}-{key}'] = value
        return self.client.post(self.url, payload, follow=True)

    def test_step1_get_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parents/parents_form.html')

    def test_full_wizard_submission_creates_parents_sheet(self):
        response = self._post_step(0, {
            'child_first_name': 'Max',
            'child_last_name': 'Mustermann',
            'health_assurance': 'AOK',
        })
        self.assertEqual(response.status_code, 200)

        response = self._post_step(1, {})
        self.assertEqual(response.status_code, 200)

        response = self._post_step(2, {})
        self.assertEqual(response.status_code, 200)

        response = self._post_step(3, {})
        self.assertEqual(response.status_code, 200)

        response = self._post_step(4, {})
        self.assertEqual(response.status_code, 200)

        response = self._post_step(5, {})
        self.assertRedirects(response, '/parents/success/')

        self.assertEqual(Parents_sheet.objects.count(), 1)
        parents_sheet = Parents_sheet.objects.get()
        self.assertEqual(parents_sheet.child_first_name, 'Max')
        self.assertEqual(parents_sheet.child_last_name, 'Mustermann')
        self.assertEqual(parents_sheet.health_assurance, 'AOK')
        self.assertFalse(parents_sheet.sheet_created)

    def test_success_page_renders(self):
        response = self.client.get(reverse('parents:success_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parents/success.html')


class ParentsSheetListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.open_sheet = Parents_sheet.objects.create(
            child_first_name='Max', child_last_name='Mustermann', sheet_created=False)
        cls.done_sheet = Parents_sheet.objects.create(
            child_first_name='Erika', child_last_name='Musterfrau', sheet_created=True)

    def test_list_shows_only_open_sheets(self):
        response = self.client.get(reverse('parents:parents_sheet_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parents/parents_sheet_liste.html')
        sheets = list(response.context['parents_sheet_list'])
        self.assertIn(self.open_sheet, sheets)
        self.assertNotIn(self.done_sheet, sheets)


class ParentsSheetUpdateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parents_sheet = Parents_sheet.objects.create(
            child_first_name='Max', child_last_name='Mustermann')

    def test_get_edit_form(self):
        response = self.client.get(
            reverse('parents:parents_sheet_edit', kwargs={'pk': self.parents_sheet.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parents/parents_sheet_detail_form.html')

    def test_post_updates_and_redirects_to_list(self):
        response = self.client.post(
            reverse('parents:parents_sheet_edit', kwargs={'pk': self.parents_sheet.pk}),
            data={'child_first_name': 'Maxi', 'child_last_name': 'Mustermann'},
        )
        self.assertRedirects(response, reverse('parents:parents_sheet_list'))
        self.parents_sheet.refresh_from_db()
        self.assertEqual(self.parents_sheet.child_first_name, 'Maxi')


class GenerateQrCodeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {'username': 'testuser', 'password': 'testpassword'}
        User.objects.create_user(**cls.credentials)

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('parents:parents_qr_code'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_logged_in_user_sees_qr_code(self):
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        self.client.post('/accounts/login/', data=self.credentials, follow=True)
        response = self.client.get(reverse('parents:parents_qr_code'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'parents/parents_qr_code.html')
        self.assertIn('qr_code', response.context)
        self.assertIn('/parents/parents-sheet/', response.context['temp_link'])

    def test_post_sends_email_with_temp_link(self):
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        self.client.post('/accounts/login/', data=self.credentials, follow=True)
        response = self.client.post(reverse('parents:parents_qr_code'), data={
            'email': 'eltern@example.com',
            'temp_link': 'http://127.0.0.1:8000/parents/parents-sheet/abc/',
            'qr_code': 'ZmFrZS1xci1jb2Rl',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['success'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('eltern@example.com', mail.outbox[0].to)
        self.assertIn('http://127.0.0.1:8000/parents/parents-sheet/abc/', mail.outbox[0].body)


class MoveParentsSheetToDocumentTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.media_root = tempfile.mkdtemp()
        cls.media_root_override = override_settings(MEDIA_ROOT=cls.media_root)
        cls.media_root_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.media_root_override.disable()
        shutil.rmtree(cls.media_root, ignore_errors=True)
        super().tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.patient = Patient.objects.create(
            pa_first_name='Max',
            pa_last_name='Mustermann',
            pa_street='Teststrasse 1',
            pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02',
        )
        cls.parents_sheet = Parents_sheet.objects.create(
            child_first_name='Max', child_last_name='Mustermann', sheet_created=False)

        cls.credentials = {'username': 'testuser', 'password': 'testpassword'}
        cls.user = User.objects.create_user(**cls.credentials)
        cls.user.user_permissions.add(Permission.objects.get(codename='add_patient'))

    def test_anonymous_user_is_redirected(self):
        response = self.client.post(
            reverse('parents:move_parents_sheet', kwargs={'pk': self.parents_sheet.pk}),
            data={'patientId': self.patient.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authorized_user_creates_document_and_marks_sheet_created(self):
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        self.client.post('/accounts/login/', data=self.credentials, follow=True)
        response = self.client.post(
            reverse('parents:move_parents_sheet', kwargs={'pk': self.parents_sheet.pk}),
            data={'patientId': self.patient.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/reports/patient/{self.patient.id}/')

        self.parents_sheet.refresh_from_db()
        self.assertTrue(self.parents_sheet.sheet_created)

        document = Document.objects.get(patient=self.patient)
        self.assertTrue(document.parents_form)
        self.assertEqual(document.description, 'Elternbogen')

        latest_history = self.parents_sheet.history.first()
        self.assertEqual(latest_history.history_user, self.user)
        self.assertTrue(latest_history.sheet_created)
