from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, Client
from django.urls import reverse
from reports.models import Doctor, Therapist, Diagnostic_group, Patient, Therapy, Therapy_report, Process_report, \
    InitialAssessment, Document, Document_therapy, Therapy_Something, Patient_Something, Login_Failed, \
    Login_User_Agent, Wait_list, Shortcuts

import json


class BasicViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.credentials = {
            'username': 'testuser_Leitung',
            'password': 'testuser_Leitung',
            'email': 'logopakt@logoeu.uber.space'}

        User.objects.create_user(**cls.credentials)

        cls.credentials = {
            'username': 'testuser_Mitarbeiter',
            'password': 'testuser_Mitarbeiter',
            'email': 'logopakt@logoeu.uber.space'}

        User.objects.create_user(**cls.credentials)

        cls.credentials = {
            'username': 'testuser_Fachadmin',
            'password': 'testuser_Fachadmin',
            'email': 'logopakt@logoeu.uber.space'}

        User.objects.create_user(**cls.credentials)

        Group_Leitung, created = Group.objects.get_or_create(name='Leitung')
        Group_Mitarbeiter, created = Group.objects.get_or_create(name='Mitarbeiter')
        Group_Fachadmin, created = Group.objects.get_or_create(name='Fachadmin')

        Group_Leitung.user_set.add(1)
        Group_Mitarbeiter.user_set.add(2)
        Group_Fachadmin.user_set.add(3)

        view_patient = Permission.objects.get(codename='view_patient')
        add_doctor = Permission.objects.get(codename='add_doctor')
        change_doctor = Permission.objects.get(codename='change_doctor')
        view_doctor = Permission.objects.get(codename='view_doctor')

        Group_Leitung.permissions.add(add_doctor)
        Group_Leitung.permissions.add(change_doctor)
        Group_Leitung.permissions.add(view_doctor)
        Group_Leitung.permissions.add(view_patient)
        Group_Mitarbeiter.permissions.add(view_patient)

        Login_Failed.objects.create(
            ipaddress='127.0.0.1',
            user_name='testuser2'
        )

        Login_User_Agent.objects.create(
            user_name='testuser',
            ip_address='127.0.0.1',
            user_agent='Test-Client'
        )

        Doctor.objects.create(
            doctor_name1='Dr. Heilende Hände',
            doctor_name2='Fr. Dr. Gute Fee',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
        )
        Therapist.objects.create(
            tp_first_name='testuser',
            tp_last_name='Mitarbeiter',
            tp_initial='tmi',
            tp_user_logopakt='testuser_Mitarbeiter'
        )
        Therapist.objects.create(
            tp_first_name='testuser',
            tp_last_name='Leitung',
            tp_initial='tle',
            tp_user_logopakt=''
        )
        Patient.objects.create(
            pa_first_name='Max',
            pa_last_name='Mustermann',
            pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02'
        )
        Therapy.objects.create(
            recipe_date='2020-03-03',
            therapy_regulation_amount=5,
            therapy_icd_cod='icd1',
            therapy_icd_cod_2='icd2',
            patients_id='1',
            therapy_doctor_id='1',
            diagnostic_group_id='1'
        )
        Therapy_Something.objects.create(
            something_else='something else description',
            therapy_id='1'
        )

    def setUp(self):
        pass

    #############################      Test basics             #############################
    def test_impressum_list(self):
        response = self.client.get(reverse('reports:impressum'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/impressum.html')

    def test_index_list(self):
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser_Mitarbeiter', 'password': 'testuser_Mitarbeiter'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.get(reverse('reports:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/index.html')

    def test_open_reports_found_user(self):
        print(f"########## Start test_open_reports         ##########")
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser_Mitarbeiter', 'password': 'testuser_Mitarbeiter'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.get(reverse('reports:open_reports'))
        self.assertEqual(response.status_code, 200)
        print(f"########## end test_open_reports           ##########")

    def test_open_reports_not_found_user(self):
        print(f"########## Start test_open_reports 2       ##########")
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser_Leitung', 'password': 'testuser_Leitung'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.get(reverse('reports:open_reports'))
        self.assertEqual(response.status_code, 200)
        print(f"########## end test_open_reports 2         ##########")

    #############################      Test doctor             #############################
    def test_doctor_list(self):
        print(f"########### Test Start doctor              ###########")

        # login
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser_Leitung', 'password': 'testuser_Leitung'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)

        # add_doctor
        response = self.client.post(reverse('reports:add_doctor'), data={
            'doctor_name1': 'Dr. Heilende Hände2',
            'doctor_street': 'Arztstrasse',
            'doctor_zip_code': '53879',
            'doctor_city': 'Euskirchen',
            'doctor_lanr': '123456780'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/doctor.html')
        self.assertContains(response, "Dr. Heilende Hände2")

        # view_doctor
        response = self.client.get(reverse('reports:doctor', kwargs={'id': '1'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/doctor.html')

        response = self.client.get(reverse('reports:doctor', kwargs={'id': '2'}), follow=True)
        self.assertEqual(response.status_code, 200)

        # search_doctor_start
        response = self.client.get(reverse('reports:search_doctor_start'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/doctor_search.html')

        # search_doctor
        response = self.client.post(reverse('reports:search_doctor'),
                                    data={'name1': '', 'lanr': '123456789'}, follow=True)
        # self.assertEqual(response.request.get("PATH_INFO"), '/reports/doctor/1/')
        self.assertEqual(response.status_code, 200)

        # edit_doctor
        response = self.client.get(reverse('reports:edit_doctor', kwargs={'id': '2'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/doctor_form.html')
        self.assertNotContains(response, "Ihr Account hat keinen Zugriff")
        response = self.client.post(reverse('reports:edit_doctor', kwargs={'id': '2'}), {
            'doctor_name1': 'Dr. Heilende Hände3',
            'doctor_street': 'Arztstrasse',
            'doctor_zip_code': '53879',
            'doctor_city': 'Euskirchen',
            'doctor_lanr': '123456780'
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/doctor.html')
        self.assertContains(response, "Dr. Heilende Hände3")

        # doctor
        response = self.client.get(reverse('reports:doctor', kwargs={'id': '10'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Patient suchen:")

        print(f"########### Test End doctor                ###########")

    #############################      Test therapist          #############################

    #############################    Test Diagnostic_group     #############################

    #############################    Test Diagnostic_group     #############################

    #############################      Test patient            #############################
    def test_patient_list(self):
        self.client = Client(HTTP_USER_AGENT='Test-Client')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'testuser_Mitarbeiter', 'password': 'testuser_Mitarbeiter'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)
        response = self.client.get(reverse('reports:patient', kwargs={'id': '1'}), follow=True)
        # print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reports/patient.html')

    #############################    Test pa_something         #############################

    #############################    Test ia                   #############################

    #############################    Test therapy_something    #############################

    #############################    Test therapy              #############################

    #############################    Test process_report       #############################

    #############################    Test therapy_report       #############################

    #############################    Test waitlist             #############################

    #############################    Test document             #############################

    #############################    Test document_therapy     #############################

    #############################    Test get_session_timer    #############################

    #############################    Test getOpenReports       #############################

    #############################    Test phone_design         #############################

    #############################    Test send_personal_mail   #############################

    #############################    Test login                #############################


class JsonServicesTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        pass

    def test_list_meta_info(self):
        response = self.client.get(reverse('reports:list_meta_info'))
        self.assertEqual(response.status_code, 200)

    def test_readShortcuts(self):
        response = self.client.get(reverse('reports:shortcuts'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('reports:shortcuts'))
        self.assertEqual(response.status_code, 400)
