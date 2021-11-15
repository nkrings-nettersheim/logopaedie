from django.db import models
from django.test import TestCase
from reports.models import Doctor, Therapist, Wait_list


class DoctorModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Doctor.objects.create(
            doctor_name1='Norbert',
            doctor_name2='Krings',
            doctor_lanr='123456789'
        )

    def test_doctor_str(self):
        doctor = Doctor.objects.get(id=1)
        self.assertEqual(str(doctor), '123456789')


class TherapistModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Therapist.objects.create(
            tp_first_name='Norbert',
            tp_last_name='Krings',
            tp_initial='nkr'
        )

    def test_therapist_str(self):
        therapist = Therapist.objects.get(id=1)
        self.assertEqual(str(therapist), 'nkr')


class WaitListModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Wait_list.objects.create(
            wl_first_name='Norbert',
            wl_last_name='Krings',
            wl_city='Nettersheim',
            wl_gender='1'
        )

    # check self_return
    def test_Wait_list_self_return(self):
        wait_list = Wait_list.objects.get(id=1)
        first_name = wait_list.wl_first_name
        last_name = wait_list.wl_last_name
        city = wait_list.wl_city
        self.assertEquals(str(wait_list), "Krings Norbert; Nettersheim")

    # check if field exists ###########################################################
    def test_it_has_information_fields(self):
        wait_list = Wait_list.objects.get(id=1)
        self.assertIsInstance(wait_list.wl_first_name, str)
        self.assertIsInstance(wait_list.wl_last_name, str)
        self.assertIsInstance(wait_list.wl_street, str)
        self.assertIsInstance(wait_list.wl_zip_code, str)
        self.assertIsInstance(wait_list.wl_city, str)
        self.assertIsInstance(wait_list.wl_phone, str)
        self.assertIsInstance(wait_list.wl_cell_phone, str)
        self.assertIsInstance(wait_list.wl_cell_phone_add1, str)
        self.assertIsInstance(wait_list.wl_cell_phone_add2, str)
        self.assertIsInstance(wait_list.wl_cell_phone_sms, str)
        self.assertIsInstance(wait_list.wl_email, str)
        self.assertIsInstance(wait_list.wl_date_of_birth, str)
        self.assertIsInstance(wait_list.wl_gender, str)
        self.assertIsInstance(wait_list.wl_call_for, str)
        self.assertIsInstance(wait_list.wl_contact_person, str)
        self.assertIsInstance(wait_list.wl_information, str)
        self.assertIsInstance(wait_list.wl_diagnostic, str)
        self.assertIsInstance(wait_list.wl_appointment, str)
        self.assertIsInstance(wait_list.wl_insurance, str)
        self.assertIsInstance(wait_list.wl_recipe, str)


    # check label #################################################################################

    def test_wl_first_name_label(self):
        wait_list = Wait_list.objects.get(id=1)
        field_label = wait_list._meta.get_field('wl_first_name').verbose_name
        self
