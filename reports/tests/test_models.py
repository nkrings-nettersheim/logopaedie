from django.db import models
from datetime import date, datetime
from django.test import TestCase
from reports.models import Doctor, Therapist, Diagnostic_group, Patient, Therapy, Therapy_report, Process_report, \
    InitialAssessment, Document, Document_therapy, Therapy_Something, Patient_Something, Login_Failed, \
    Login_User_Agent, Wait_list, Shortcuts


class DoctorModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )

    # has information
    def test_it_has_information_fields(self):
        doctor = Doctor.objects.get(id=1)
        self.assertIsInstance(doctor.doctor_name1, str)
        self.assertIsInstance(doctor.doctor_name2, str)
        self.assertIsInstance(doctor.doctor_name3, str)
        self.assertIsInstance(doctor.doctor_street, str)
        self.assertIsInstance(doctor.doctor_zip_code, str)
        self.assertIsInstance(doctor.doctor_city, str)
        self.assertIsInstance(doctor.doctor_lanr, str)
        self.assertIsInstance(doctor.created_at, datetime)
        self.assertIsInstance(doctor.updated_at, datetime)

    # test label
    def test_doctor_name1_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_name1').verbose_name
        self.assertEqual(field_label, 'doctor name1')

    def test_doctor_name2_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_name2').verbose_name
        self.assertEqual(field_label, 'doctor name2')

    def test_doctor_name3_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_name3').verbose_name
        self.assertEqual(field_label, 'doctor name3')

    def test_doctor_street_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_street').verbose_name
        self.assertEqual(field_label, 'doctor street')

    def test_doctor_zip_code_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_zip_code').verbose_name
        self.assertEqual(field_label, 'doctor zip code')

    def test_doctor_city_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_city').verbose_name
        self.assertEqual(field_label, 'doctor city')

    def test_doctor_lanr_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('doctor_lanr').verbose_name
        self.assertEqual(field_label, 'doctor lanr')

    def test_created_at_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        doctor = Doctor.objects.get(id=1)
        field_label = doctor._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_doctor_name1_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_name1').max_length
        self.assertEqual(max_length, 75)

    def test_doctor_name2_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_name2').max_length
        self.assertEqual(max_length, 75)

    def test_doctor_name3_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_name3').max_length
        self.assertEqual(max_length, 75)

    def test_doctor_street_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_street').max_length
        self.assertEqual(max_length, 50)

    def test_doctor_zip_code_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_zip_code').max_length
        self.assertEqual(max_length, 5)

    def test_doctor_city_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_city').max_length
        self.assertEqual(max_length, 50)

    def test_doctor_lanr_max_length(self):
        doctor = Doctor.objects.get(id=1)
        max_length = doctor._meta.get_field('doctor_lanr').max_length
        self.assertEqual(max_length, 9)

    # test objects
    def test_doctor_str(self):
        doctor = Doctor.objects.get(id=1)
        expected_object_name = f'{doctor.doctor_lanr}'
        self.assertEqual(expected_object_name, str(doctor))


class TherapistModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Therapist.objects.create(
            tp_first_name='Max',
            tp_last_name='Mustermann',
            tp_initial='mmu'
        )

    # has information
    def test_it_has_information_fields(self):
        therapist = Therapist.objects.get(id=1)
        self.assertIsInstance(therapist.tp_first_name, str)
        self.assertIsInstance(therapist.tp_last_name, str)
        self.assertIsInstance(therapist.tp_initial, str)
        self.assertIsInstance(therapist.tp_user_logopakt, str)
        self.assertIsInstance(therapist.created_at, datetime)
        self.assertIsInstance(therapist.updated_at, datetime)

    # test label
    def test_tp_first_name_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('tp_first_name').verbose_name
        self.assertEqual(field_label, 'tp first name')

    def test_tp_last_name_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('tp_last_name').verbose_name
        self.assertEqual(field_label, 'tp last name')

    def test_tp_initial_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('tp_initial').verbose_name
        self.assertEqual(field_label, 'tp initial')

    def test_tp_user_logopakt_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('tp_user_logopakt').verbose_name
        self.assertEqual(field_label, 'tp user logopakt')

    def test_created_at_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        therapist = Therapist.objects.get(id=1)
        field_label = therapist._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_tp_first_name_max_length(self):
        therapist = Therapist.objects.get(id=1)
        max_length = therapist._meta.get_field('tp_first_name').max_length
        self.assertEqual(max_length, 50)

    def test_tp_last_name_max_length(self):
        therapist = Therapist.objects.get(id=1)
        max_length = therapist._meta.get_field('tp_last_name').max_length
        self.assertEqual(max_length, 50)

    def test_tp_initial_max_length(self):
        therapist = Therapist.objects.get(id=1)
        max_length = therapist._meta.get_field('tp_initial').max_length
        self.assertEqual(max_length, 5)

    def test_tp_user_logopakt_max_length(self):
        therapist = Therapist.objects.get(id=1)
        max_length = therapist._meta.get_field('tp_user_logopakt').max_length
        self.assertEqual(max_length, 20)

    # test objects
    def test_therapist_str(self):
        therapist = Therapist.objects.get(id=1)
        expected_object_name = f'{therapist.tp_initial}'
        self.assertEqual(expected_object_name, str(therapist))


class Diagnostic_groupModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
        )

    # check if field exists ###########################################################
    def test_it_has_information_fields(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        self.assertIsInstance(diagnostic_group.diagnostic_key, str)
        self.assertIsInstance(diagnostic_group.diagnostic_description, str)
        self.assertIsInstance(diagnostic_group.diagnostic_max_therapy, int)

    # test label
    def test_diagnostic_key_label(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        field_label = diagnostic_group._meta.get_field('diagnostic_key').verbose_name
        self.assertEqual(field_label, 'diagnostic key')

    def test_diagnostic_description_label(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        field_label = diagnostic_group._meta.get_field('diagnostic_description').verbose_name
        self.assertEqual(field_label, 'diagnostic description')

    def test_diagnostic_max_therapy_label(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        field_label = diagnostic_group._meta.get_field('diagnostic_max_therapy').verbose_name
        self.assertEqual(field_label, 'diagnostic max therapy')

    # test max_length
    def test_diagnostic_key_max_length(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        max_length = diagnostic_group._meta.get_field('diagnostic_key').max_length
        self.assertEqual(max_length, 10)

    def test_diagnostic_description_max_length(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        max_length = diagnostic_group._meta.get_field('diagnostic_description').max_length
        self.assertEqual(max_length, 250)

    # test objects
    def test_diagnostic_group_str(self):
        diagnostic_group = Diagnostic_group.objects.get(id=1)
        expected_object_name = f'{diagnostic_group.diagnostic_key}'
        self.assertEqual(expected_object_name, str(diagnostic_group))


class PatientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Patient.objects.create(
            pa_first_name='Max',
            pa_last_name='Mustermann',
            pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02'
        )

    # has information
    def test_it_has_information_fields(self):
        patient = Patient.objects.get(id=1)
        self.assertIsInstance(patient.pa_first_name, str)
        self.assertIsInstance(patient.pa_last_name, str)
        self.assertIsInstance(patient.pa_street, str)
        self.assertIsInstance(patient.pa_zip_code, str)
        self.assertIsInstance(patient.pa_city, str)
        self.assertIsInstance(patient.pa_phone, str)
        self.assertIsInstance(patient.pa_cell_phone, str)
        self.assertIsInstance(patient.pa_cell_phone_add1, str)
        self.assertIsInstance(patient.pa_cell_phone_add2, str)
        self.assertIsInstance(patient.pa_cell_phone_sms, str)
        self.assertIsInstance(patient.pa_email, str)
        self.assertIsInstance(patient.pa_date_of_birth, date)
        self.assertIsInstance(patient.pa_gender, str)
        self.assertIsInstance(patient.pa_attention, str)
        self.assertIsInstance(patient.pa_allergy, str)
        self.assertIsInstance(patient.pa_note, str)
        self.assertIsInstance(patient.pa_active_no_yes, bool)
        self.assertIsInstance(patient.pa_invoice_mail, bool)
        self.assertIsInstance(patient.pa_sms_no_yes, bool)
        self.assertIsInstance(patient.pa_email_no_yes, bool)
        self.assertIsInstance(patient.created_at, datetime)
        self.assertIsInstance(patient.updated_at, datetime)

    # test label
    def test_pa_first_name_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_first_name').verbose_name
        self.assertEqual(field_label, 'pa first name')

    def test_pa_last_name_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_last_name').verbose_name
        self.assertEqual(field_label, 'pa last name')

    def test_pa_street_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_street').verbose_name
        self.assertEqual(field_label, 'pa street')

    def test_pa_zip_code_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_zip_code').verbose_name
        self.assertEqual(field_label, 'pa zip code')

    def test_pa_city_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_city').verbose_name
        self.assertEqual(field_label, 'pa city')
        
    def test_pa_phone_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_phone').verbose_name
        self.assertEqual(field_label, 'pa phone')

    def test_pa_cell_phone_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_cell_phone').verbose_name
        self.assertEqual(field_label, 'pa cell phone')

    def test_pa_cell_phone_add1_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_cell_phone_add1').verbose_name
        self.assertEqual(field_label, 'pa cell phone add1')

    def test_pa_cell_phone_add2_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_cell_phone_add2').verbose_name
        self.assertEqual(field_label, 'pa cell phone add2')

    def test_pa_cell_phone_sms_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_cell_phone_sms').verbose_name
        self.assertEqual(field_label, 'pa cell phone sms')

    def test_pa_email_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_email').verbose_name
        self.assertEqual(field_label, 'pa email')

    def test_pa_date_of_birth_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_date_of_birth').verbose_name
        self.assertEqual(field_label, 'pa date of birth')

    def test_pa_gender_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_gender').verbose_name
        self.assertEqual(field_label, 'pa gender')

    def test_pa_attention_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_attention').verbose_name
        self.assertEqual(field_label, 'pa attention')

    def test_pa_allergy_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_allergy').verbose_name
        self.assertEqual(field_label, 'pa allergy')

    def test_pa_note_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_note').verbose_name
        self.assertEqual(field_label, 'pa note')

    def test_pa_active_no_yes_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_active_no_yes').verbose_name
        self.assertEqual(field_label, 'pa active no yes')

    def test_pa_invoice_mail_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_invoice_mail').verbose_name
        self.assertEqual(field_label, 'pa invoice mail')

    def test_pa_sms_no_yes_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_sms_no_yes').verbose_name
        self.assertEqual(field_label, 'pa sms no yes')

    def test_pa_email_no_yes_label(self):
        patient = Patient.objects.get(id=1)
        field_label = patient._meta.get_field('pa_email_no_yes').verbose_name
        self.assertEqual(field_label, 'pa email no yes')

    # test max_length
    def test_pa_first_name_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_first_name').max_length
        self.assertEqual(max_length, 50)

    def test_pa_last_name_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_last_name').max_length
        self.assertEqual(max_length, 50)

    def test_pa_street_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_street').max_length
        self.assertEqual(max_length, 100)

    def test_pa_zip_code_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_zip_code').max_length
        self.assertEqual(max_length, 10)

    def test_pa_city_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_city').max_length
        self.assertEqual(max_length, 255)

    def test_pa_cell_phone_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_cell_phone').max_length
        self.assertEqual(max_length, 100)

    def test_pa_cell_phone_add1_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_cell_phone_add1').max_length
        self.assertEqual(max_length, 100)

    def test_pa_cell_phone_add2_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_cell_phone_add2').max_length
        self.assertEqual(max_length, 100)

    def test_pa_cell_phone_sms_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_cell_phone_sms').max_length
        self.assertEqual(max_length, 100)

    def test_pa_email_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_email').max_length
        self.assertEqual(max_length, 254)

    def test_pa_gender_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_gender').max_length
        self.assertEqual(max_length, 1)

    def test_pa_attention_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_attention').max_length
        self.assertEqual(max_length, 100)

    def test_pa_allergy_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_allergy').max_length
        self.assertEqual(max_length, 100)

    def test_pa_note_max_length(self):
        patient = Patient.objects.get(id=1)
        max_length = patient._meta.get_field('pa_note').max_length
        self.assertEqual(max_length, 255)

    # test objects
    def test_patient_str(self):
        patient = Patient.objects.get(id=1)
        expected_object_name = f'{patient.pa_last_name} {patient.pa_first_name}; {patient.pa_city}'
        self.assertEqual(expected_object_name, str(patient))


class TherapyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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

    # has information
    def test_it_has_information_fields(self):
        therapy = Therapy.objects.get(id=1)
        self.assertIsInstance(therapy.recipe_date, date)
        self.assertIsInstance(therapy.therapy_regulation_amount, int)
        self.assertIsInstance(therapy.therapy_duration, str)
        self.assertIsInstance(therapy.therapy_frequence, str)
        self.assertIsInstance(therapy.therapy_rid_of, bool)
        self.assertIsInstance(therapy.therapy_report_no_yes, bool)
        self.assertIsInstance(therapy.therapy_homevisit_no_yes, bool)
        self.assertIsInstance(therapy.therapy_indication_key, str)
        self.assertIsInstance(therapy.therapy_icd_cod, str)
        self.assertIsInstance(therapy.therapy_icd_cod_2, str)
        self.assertIsInstance(therapy.therapy_icd_cod_3, str)
        self.assertIsInstance(therapy.therapy_doctor, object)
        self.assertIsInstance(therapy.created_at, datetime)
        self.assertIsInstance(therapy.updated_at, datetime)
        self.assertIsInstance(therapy.patients, object)
        self.assertIsInstance(therapy.therapists, object)
        self.assertIsInstance(therapy.diagnostic_group, object)
        self.assertIsInstance(therapy.first_diagnostic_no_yes, bool)
        self.assertIsInstance(therapy.need_diagnostic_no_yes, bool)
        self.assertIsInstance(therapy.continue_diagnostic_no_yes, bool)

    # test label
    def test_recipe_date_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('recipe_date').verbose_name
        self.assertEqual(field_label, 'recipe date')

    def test_therapy_regulation_amount_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_regulation_amount').verbose_name
        self.assertEqual(field_label, 'therapy regulation amount')

    def test_therapy_duration_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_duration').verbose_name
        self.assertEqual(field_label, 'therapy duration')

    def test_therapy_frequence_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_frequence').verbose_name
        self.assertEqual(field_label, 'therapy frequence')

    def test_therapy_rid_of_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_rid_of').verbose_name
        self.assertEqual(field_label, 'therapy rid of')

    def test_therapy_report_no_yes_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_report_no_yes').verbose_name
        self.assertEqual(field_label, 'therapy report no yes')

    def test_therapy_homevisit_no_yes_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_homevisit_no_yes').verbose_name
        self.assertEqual(field_label, 'therapy homevisit no yes')

    def test_therapy_indication_key_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_indication_key').verbose_name
        self.assertEqual(field_label, 'therapy indication key')

    def test_therapy_icd_cod_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_icd_cod').verbose_name
        self.assertEqual(field_label, 'therapy icd cod')

    def test_therapy_icd_cod_2_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_icd_cod_2').verbose_name
        self.assertEqual(field_label, 'therapy icd cod 2')

    def test_therapy_icd_cod_3_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_icd_cod_3').verbose_name
        self.assertEqual(field_label, 'therapy icd cod 3')

    def test_therapy_doctor_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapy_doctor').verbose_name
        self.assertEqual(field_label, 'therapy doctor')

    def test_created_at_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    def test_patients_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('patients').verbose_name
        self.assertEqual(field_label, 'patients')

    def test_therapists_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('therapists').verbose_name
        self.assertEqual(field_label, 'therapists')

    def test_diagnostic_group_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('diagnostic_group').verbose_name
        self.assertEqual(field_label, 'diagnostic group')

    def test_first_diagnostic_no_yes_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('first_diagnostic_no_yes').verbose_name
        self.assertEqual(field_label, 'first diagnostic no yes')

    def test_need_diagnostic_no_yes_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('need_diagnostic_no_yes').verbose_name
        self.assertEqual(field_label, 'need diagnostic no yes')

    def test_continue_diagnostic_no_yes_label(self):
        therapy = Therapy.objects.get(id=1)
        field_label = therapy._meta.get_field('continue_diagnostic_no_yes').verbose_name
        self.assertEqual(field_label, 'continue diagnostic no yes')

    # test max_length
    def test_therapy_duration_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_duration').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_frequence_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_frequence').max_length
        self.assertEqual(max_length, 5)

    def test_therapy_indication_key_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_indication_key').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_icd_cod_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_icd_cod').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_icd_cod_2_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_icd_cod_2').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_icd_cod_3_max_length(self):
        therapy = Therapy.objects.get(id=1)
        max_length = therapy._meta.get_field('therapy_icd_cod_3').max_length
        self.assertEqual(max_length, 10)

    # test objects
    def test_therapy_str(self):
        therapy = Therapy.objects.get(id=1)
        expected_object_name = f'{therapy.recipe_date}'
        self.assertEqual(expected_object_name, str(therapy))


class TherapyReportModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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
        Therapy_report.objects.create(
            report_date='2020-03-03',
            therapy_start='2020-02-03',
            therapy_end='2020-03-03',
            therapy_id='1'
        )

    # has information
    def test_it_has_information_fields(self):
        therapy_report = Therapy_report.objects.get(id=1)
        self.assertIsInstance(therapy_report.report_date, date)
        self.assertIsInstance(therapy_report.therapy_start, date)
        self.assertIsInstance(therapy_report.therapy_end, date)
        self.assertIsInstance(therapy_report.therapy_current_result, str)
        self.assertIsInstance(therapy_report.therapy_emphases, str)
        self.assertIsInstance(therapy_report.therapy_forecast, str)
        self.assertIsInstance(therapy_report.therapy_indicated, bool)
        self.assertIsInstance(therapy_report.therapy_break, bool)
        self.assertIsInstance(therapy_report.therapy_break_internal, bool)
        self.assertIsInstance(therapy_report.therapy_break_date, date)
        self.assertIsInstance(therapy_report.therapy_comment, str)
        self.assertIsInstance(therapy_report.therapy_individual, bool)
        self.assertIsInstance(therapy_report.therapy_individual_min, str)
        self.assertIsInstance(therapy_report.therapy_group, bool)
        self.assertIsInstance(therapy_report.therapy_group_min, str)
        self.assertIsInstance(therapy_report.therapy_finish, bool)
        self.assertIsInstance(therapy_report.therapy_re_introduction, bool)
        self.assertIsInstance(therapy_report.therapy_re_introduction_weeks, int)
        self.assertIsInstance(therapy_report.therapy_frequence, bool)
        self.assertIsInstance(therapy_report.therapy_frequence_count_per_week, str)
        self.assertIsInstance(therapy_report.therapy_another, bool)
        self.assertIsInstance(therapy_report.therapy_another_text, str)
        self.assertIsInstance(therapy_report.therapy_home_visit, bool)
        self.assertIsInstance(therapy_report.therapy_necessary, bool)
        self.assertIsInstance(therapy_report.therapy_summary, str)
        self.assertIsInstance(therapy_report.therapy_request_of, str)
        self.assertIsInstance(therapy_report.therapy_insurance, str)
        self.assertIsInstance(therapy_report.therapy_diagnostic, str)
        self.assertIsInstance(therapy_report.therapy_doc_diagnostic, str)
        self.assertIsInstance(therapy_report.therapy_therapist_diagnostic, str)
        self.assertIsInstance(therapy_report.therapy_status, str)
        self.assertIsInstance(therapy_report.therapy_aims, str)
        self.assertIsInstance(therapy_report.therapy_content, str)
        self.assertIsInstance(therapy_report.therapy_process, str)
        self.assertIsInstance(therapy_report.therapy_compliance, str)
        self.assertIsInstance(therapy_report.therapy_report_variation, int)

    # test label
    def test_report_date_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('report_date').verbose_name
        self.assertEqual(field_label, 'report date')

    def test_therapy_start_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_start').verbose_name
        self.assertEqual(field_label, 'therapy start')

    def test_therapy_end_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_end').verbose_name
        self.assertEqual(field_label, 'therapy end')

    def test_therapy_current_result_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_current_result').verbose_name
        self.assertEqual(field_label, 'therapy current result')

    def test_therapy_emphases_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_emphases').verbose_name
        self.assertEqual(field_label, 'therapy emphases')

    def test_therapy_forecast_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_forecast').verbose_name
        self.assertEqual(field_label, 'therapy forecast')

    def test_therapy_indicated_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_indicated').verbose_name
        self.assertEqual(field_label, 'therapy indicated')

    def test_therapy_break_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_break').verbose_name
        self.assertEqual(field_label, 'therapy break')

    def test_therapy_break_internal_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_break_internal').verbose_name
        self.assertEqual(field_label, 'therapy break internal')

    def test_therapy_break_date_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_break_date').verbose_name
        self.assertEqual(field_label, 'therapy break date')

    def test_therapy_comment_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_comment').verbose_name
        self.assertEqual(field_label, 'therapy comment')

    def test_therapy_individual_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_individual').verbose_name
        self.assertEqual(field_label, 'therapy individual')

    def test_therapy_individual_min_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_individual_min').verbose_name
        self.assertEqual(field_label, 'therapy individual min')

    def test_therapy_group_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_group').verbose_name
        self.assertEqual(field_label, 'therapy group')

    def test_therapy_group_min_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_group_min').verbose_name
        self.assertEqual(field_label, 'therapy group min')

    def test_therapy_finish_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_finish').verbose_name
        self.assertEqual(field_label, 'therapy finish')

    def test_therapy_re_introduction_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_re_introduction').verbose_name
        self.assertEqual(field_label, 'therapy re introduction')

    def test_therapy_re_introduction_weeks_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_re_introduction_weeks').verbose_name
        self.assertEqual(field_label, 'therapy re introduction weeks')

    def test_therapy_frequence_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_frequence').verbose_name
        self.assertEqual(field_label, 'therapy frequence')

    def test_therapy_frequence_count_per_week_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_frequence_count_per_week').verbose_name
        self.assertEqual(field_label, 'therapy frequence count per week')

    def test_therapy_another_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_another').verbose_name
        self.assertEqual(field_label, 'therapy another')

    def test_therapy_another_text_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_another_text').verbose_name
        self.assertEqual(field_label, 'therapy another text')

    def test_therapy_home_visit_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_home_visit').verbose_name
        self.assertEqual(field_label, 'therapy home visit')

    def test_therapy_necessary_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_necessary').verbose_name
        self.assertEqual(field_label, 'therapy necessary')

    def test_therapy_summary_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_summary').verbose_name
        self.assertEqual(field_label, 'therapy summary')

    def test_therapy_request_of_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_request_of').verbose_name
        self.assertEqual(field_label, 'therapy request of')

    def test_therapy_insurance_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_insurance').verbose_name
        self.assertEqual(field_label, 'therapy insurance')

    def test_therapy_diagnostic_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_diagnostic').verbose_name
        self.assertEqual(field_label, 'therapy diagnostic')

    def test_therapy_doc_diagnostic_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_doc_diagnostic').verbose_name
        self.assertEqual(field_label, 'therapy doc diagnostic')

    def test_therapy_therapist_diagnostic_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_therapist_diagnostic').verbose_name
        self.assertEqual(field_label, 'therapy therapist diagnostic')

    def test_therapy_status_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_status').verbose_name
        self.assertEqual(field_label, 'therapy status')

    def test_therapy_aims_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_aims').verbose_name
        self.assertEqual(field_label, 'therapy aims')

    def test_therapy_content_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_content').verbose_name
        self.assertEqual(field_label, 'therapy content')

    def test_therapy_process_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_process').verbose_name
        self.assertEqual(field_label, 'therapy process')

    def test_therapy_compliance_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_compliance').verbose_name
        self.assertEqual(field_label, 'therapy compliance')

    def test_therapy_report_variation_label(self):
        therapy_report = Therapy_report.objects.get(id=1)
        field_label = therapy_report._meta.get_field('therapy_report_variation').verbose_name
        self.assertEqual(field_label, 'therapy report variation')

    # test max_length
    def test_therapy_report_comment_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_comment').max_length
        self.assertEqual(max_length, 255)

    def test_therapy_report_individual_min_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_individual_min').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_report_group_min_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_group_min').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_frequence_count_per_week_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_frequence_count_per_week').max_length
        self.assertEqual(max_length, 10)

    def test_therapy_another_text_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_another_text').max_length
        self.assertEqual(max_length, 25)

    def test_therapy_request_of_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_request_of').max_length
        self.assertEqual(max_length, 100)

    def test_therapy_insurance_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_insurance').max_length
        self.assertEqual(max_length, 100)

    def test_therapy_diagnostic_max_length(self):
        therapy_report = Therapy_report.objects.get(id=1)
        max_length = therapy_report._meta.get_field('therapy_diagnostic').max_length
        self.assertEqual(max_length, 100)

    # test objects
    def test_therapy_report_str(self):
        therapy_report = Therapy_report.objects.get(id=1)
        expected_object_name = f'{therapy_report.report_date}'
        self.assertEqual(expected_object_name, str(therapy_report))


class ProcessReportModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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
        Process_report.objects.create(
            process_treatment='1',
            process_content='Dies ist der Prozess Text',
            therapy_id='1'
        )

    # has information
    def test_it_has_information_fields(self):
        process_report = Process_report.objects.get(id=1)
        self.assertIsInstance(process_report.process_treatment, int)
        self.assertIsInstance(process_report.process_content, str)
        self.assertIsInstance(process_report.process_exercises, str)
        self.assertIsInstance(process_report.process_results, str)
        self.assertIsInstance(process_report.process_content_2, str)
        self.assertIsInstance(process_report.process_exercises_2, str)
        self.assertIsInstance(process_report.process_results_2, str)
        self.assertIsInstance(process_report.process_content_3, str)
        self.assertIsInstance(process_report.process_exercises_3, str)
        self.assertIsInstance(process_report.process_results_3, str)

    # test label
    def test_process_treatment_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_treatment').verbose_name
        self.assertEqual(field_label, 'process treatment')

    def test_process_content_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_content').verbose_name
        self.assertEqual(field_label, 'process content')      

    def test_process_exercises_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_exercises').verbose_name
        self.assertEqual(field_label, 'process exercises')

    def test_process_results_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_results').verbose_name
        self.assertEqual(field_label, 'process results')

    def test_process_content_2_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_content_2').verbose_name
        self.assertEqual(field_label, 'process content 2')

    def test_process_exercises_2_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_exercises_2').verbose_name
        self.assertEqual(field_label, 'process exercises 2')

    def test_process_results_2_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_results_2').verbose_name
        self.assertEqual(field_label, 'process results 2')

    def test_process_content_3_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_content_3').verbose_name
        self.assertEqual(field_label, 'process content 3')

    def test_process_exercises_3_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_exercises_3').verbose_name
        self.assertEqual(field_label, 'process exercises 3')

    def test_process_results_3_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('process_results_3').verbose_name
        self.assertEqual(field_label, 'process results 3')

    def test_therapy_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('therapy').verbose_name
        self.assertEqual(field_label, 'therapy')

    def test_created_at_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, 'created at')

    def test_updated_at_label(self):
        process_report = Process_report.objects.get(id=1)
        field_label = process_report._meta.get_field('updated_at').verbose_name
        self.assertEqual(field_label, 'updated at')

    # test max_length
    def test_process_content_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_content').max_length
        self.assertEqual(max_length, 255)

    def test_process_exercises_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_exercises').max_length
        self.assertEqual(max_length, 255)

    def test_process_results_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_results').max_length
        self.assertEqual(max_length, 50)

    def test_process_content_2_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_content_2').max_length
        self.assertEqual(max_length, 255)

    def test_process_exercises_2_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_exercises_2').max_length
        self.assertEqual(max_length, 255)

    def test_process_results_2_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_results_2').max_length
        self.assertEqual(max_length, 50)

    def test_process_content_3_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_content_3').max_length
        self.assertEqual(max_length, 255)

    def test_process_exercises_3_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_exercises_3').max_length
        self.assertEqual(max_length, 255)

    def test_process_results_3_max_length(self):
        process_report = Process_report.objects.get(id=1)
        max_length = process_report._meta.get_field('process_results_3').max_length
        self.assertEqual(max_length, 50)

    # test objects
    def test_process_report_str(self):
        process_report = Process_report.objects.get(id=1)
        expected_object_name = f'{process_report.process_content}'
        self.assertEqual(expected_object_name, str(process_report))


class InitialAssessmentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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
        InitialAssessment.objects.create(
            ia_date='2022-01-01',
            ia_assessment='logopakt ia',
            ia_test_date='2022-01-02',
            therapy_id='1'
        )

    # test objects
    def test_initialassessment_str(self):
        initialassessment = InitialAssessment.objects.get(id=1)
        expected_object_name = f'{initialassessment.ia_assessment}'
        self.assertEqual(expected_object_name, str(initialassessment))


class DocumentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Patient.objects.create(
            pa_first_name='Max',
            pa_last_name='Mustermann',
            pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02'
        )
        Document.objects.create(
            description='document_description',
            patient_id='1'
        )

    # test objects
    def test_document_str(self):
        document = Document.objects.get(id=1)
        expected_object_name = f'{document.description}'
        self.assertEqual(expected_object_name, str(document))


class Document_therapyModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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
        Document_therapy.objects.create(
            description='document_description',
            therapy_id='1'
        )

    # test objects
    def test_document_therapy_str(self):
        document_therapy = Document_therapy.objects.get(id=1)
        expected_object_name = f'{document_therapy.description}'
        self.assertEqual(expected_object_name, str(document_therapy))


class Therapy_SomethingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Doctor.objects.create(
            doctor_name1='Max',
            doctor_name2='Mustermann',
            doctor_lanr='123456789'
        )
        Diagnostic_group.objects.create(
            diagnostic_key='ST1',
            diagnostic_description='Organische Störungen',
            diagnostic_max_therapy='20'
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

    # test objects
    def test_something_else_str(self):
        therapy_something = Therapy_Something.objects.get(id=1)
        expected_object_name = f'{therapy_something.something_else}'
        self.assertEqual(expected_object_name, str(therapy_something))


class Patient_SomethingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Patient.objects.create(
            pa_first_name='Max',
            pa_last_name='Mustermann',
            pa_city='Musterhausen',
            pa_date_of_birth='2000-02-02'
        )
        Patient_Something.objects.create(
            pa_something_else='pa something else description',
            patient_id='1'
        )

    # test objects
    def test_patient_something_str(self):
        patient_something = Patient_Something.objects.get(id=1)
        expected_object_name = f'{patient_something.pa_something_else}'
        self.assertEqual(expected_object_name, str(patient_something))


class Login_FailedModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Login_Failed.objects.create(
            user_name='logopaktuser'
        )

    # test objects
    def test_login_failed_str(self):
        login_failed = Login_Failed.objects.get(id=1)
        expected_object_name = f'{login_failed.user_name}'
        self.assertEqual(expected_object_name, str(login_failed))


class Login_User_AgentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Login_User_Agent.objects.create(
            user_name='logopaktuser'
        )

    # test objects
    def test_login_user_agent_str(self):
        login_user_agent = Login_User_Agent.objects.get(id=1)
        expected_object_name = f'{login_user_agent.user_name}'
        self.assertEqual(expected_object_name, str(login_user_agent))


class WaitListModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Wait_list.objects.create(
            wl_first_name='Max',
            wl_last_name='Mustermann',
            wl_city='Musterhausen',
            wl_gender='1'
        )

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
        self.assertIsInstance(wait_list.wl_date_of_birth, date)
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
        self.assertEqual(field_label, 'wl first name')

    # test objects
    def test_wait_list_str(self):
        wait_list = Wait_list.objects.get(id=1)
        expected_object_name = f'{wait_list.wl_last_name} {wait_list.wl_first_name}; {wait_list.wl_city}'
        self.assertEqual(expected_object_name, str(wait_list))


class ShortcutsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Shortcuts.objects.create(
            short='SRV'
        )

    # test objects
    def test_initialassessment_str(self):
        shortcuts = Shortcuts.objects.get(id=1)
        expected_object_name = f'{shortcuts.short}'
        self.assertEqual(expected_object_name, str(shortcuts))

