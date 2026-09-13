from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory

from simple_history.middleware import HistoryRequestMiddleware

from reports.models import (Doctor, Diagnostic_group, Patient, Therapy, Therapy_report,
                            Process_report, InitialAssessment, Registration)


class HistoricalRecordsCreationTest(TestCase):
    """Prueft, dass fuer die dokumentationsrelevanten Modelle eine Historie mitgeschrieben wird."""

    @classmethod
    def setUpTestData(cls):
        cls.doctor = Doctor.objects.create(
            doctor_name1='Max', doctor_name2='Mustermann', doctor_lanr='123456789')
        cls.diagnostic_group = Diagnostic_group.objects.create(
            diagnostic_key='ST1', diagnostic_description='Organische Störungen', diagnostic_max_therapy='20')
        cls.patient = Patient.objects.create(
            pa_first_name='Max', pa_last_name='Mustermann', pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02')
        cls.therapy = Therapy.objects.create(
            recipe_date='2020-03-03', therapy_regulation_amount=5, therapy_icd_cod='icd1',
            therapy_icd_cod_2='icd2', patients_id=cls.patient.id, therapy_doctor_id=cls.doctor.id,
            diagnostic_group_id=cls.diagnostic_group.id)

    def test_patient_create_and_update_are_tracked(self):
        self.assertEqual(self.patient.history.count(), 1)
        self.assertEqual(self.patient.history.first().history_type, '+')

        self.patient.pa_city = 'Neustadt'
        self.patient.save()

        self.assertEqual(self.patient.history.count(), 2)
        latest, previous = self.patient.history.all()
        self.assertEqual(latest.history_type, '~')
        self.assertEqual(latest.pa_city, 'Neustadt')
        self.assertEqual(previous.pa_city, 'Musterhausen')

    def test_patient_delete_is_tracked(self):
        patient_id = self.patient.id
        self.patient.delete()

        history = Patient.history.filter(id=patient_id)
        self.assertEqual(history.count(), 2)
        self.assertEqual(history.first().history_type, '-')

    def test_therapy_history_tracks_icd_code_change(self):
        self.assertEqual(self.therapy.history.count(), 1)

        self.therapy.therapy_icd_cod = 'icd9'
        self.therapy.save()

        self.assertEqual(self.therapy.history.count(), 2)
        self.assertEqual(self.therapy.history.first().therapy_icd_cod, 'ICD9')

    def test_therapy_report_is_tracked(self):
        therapy_report = Therapy_report.objects.create(
            report_date='2020-03-03', therapy_start='2020-02-03', therapy_end='2020-03-03',
            therapy_id=self.therapy.id)
        self.assertEqual(therapy_report.history.count(), 1)

        therapy_report.therapy_comment = 'Kommentar geaendert'
        therapy_report.save()

        self.assertEqual(therapy_report.history.count(), 2)
        self.assertEqual(therapy_report.history.first().therapy_comment, 'Kommentar geaendert')

    def test_process_report_is_tracked(self):
        process_report = Process_report.objects.create(
            process_treatment=1, process_content='Ausgangstext', therapy_id=self.therapy.id)
        self.assertEqual(process_report.history.count(), 1)

        process_report.process_content = 'Geaenderter Text'
        process_report.save()

        self.assertEqual(process_report.history.count(), 2)
        self.assertEqual(process_report.history.first().process_content, 'Geaenderter Text')

    def test_initial_assessment_is_tracked(self):
        ia = InitialAssessment.objects.create(
            ia_date='2022-01-01', ia_assessment='logopakt ia', ia_test_date='2022-01-02',
            therapy_id=self.therapy.id)
        self.assertEqual(ia.history.count(), 1)

        ia.ia_assessment = 'geaenderte Einschaetzung'
        ia.save()

        self.assertEqual(ia.history.count(), 2)
        self.assertEqual(ia.history.first().ia_assessment, 'geaenderte Einschaetzung')

    def test_registration_is_tracked(self):
        registration = Registration.objects.create(
            reg_name='Mustermann', reg_first_name='Max', reg_date_of_birth='2000-02-02')
        self.assertEqual(registration.history.count(), 1)

        registration.reg_created = True
        registration.save()

        self.assertEqual(registration.history.count(), 2)
        self.assertTrue(registration.history.first().reg_created)


class HistoryUserAttributionTest(TestCase):
    """Prueft, dass HistoryRequestMiddleware den aendernden Benutzer an die Historie durchreicht."""

    @classmethod
    def setUpTestData(cls):
        cls.patient = Patient.objects.create(
            pa_first_name='Max', pa_last_name='Mustermann', pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02')
        cls.user = User.objects.create_user(username='fachadmin', password='fachadmin')

    def test_history_user_is_set_from_request_context(self):
        request = RequestFactory().get('/')
        request.user = self.user
        captured = {}

        def get_response(req):
            self.patient.pa_attention = 'Über Request geändert'
            self.patient.save()
            captured['history'] = self.patient.history.first()

        HistoryRequestMiddleware(get_response)(request)

        self.assertEqual(captured['history'].history_user, self.user)
        self.assertEqual(captured['history'].pa_attention, 'Über Request geändert')

    def test_history_user_is_none_without_request_context(self):
        self.patient.pa_attention = 'Ohne Request geändert'
        self.patient.save()

        self.assertIsNone(self.patient.history.first().history_user)
