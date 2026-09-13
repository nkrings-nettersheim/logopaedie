from django.test import TestCase

from parents.models import Parents_sheet


class ParentsSheetModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.parents_sheet = Parents_sheet.objects.create(
            child_first_name='Max',
            child_last_name='Mustermann',
            child_day_of_birth='2020-01-01',
        )

    def test_str_returns_last_and_first_name(self):
        self.assertEqual(str(self.parents_sheet), 'Mustermann, Max')

    def test_sheet_created_defaults_to_false(self):
        self.assertFalse(self.parents_sheet.sheet_created)

    def test_boolean_fields_default_to_true(self):
        self.assertTrue(self.parents_sheet.problems_pregnancy)
        self.assertTrue(self.parents_sheet.child_allergy)
        self.assertTrue(self.parents_sheet.child_chronic_disease)

    def test_boolean_fields_default_to_false(self):
        self.assertFalse(self.parents_sheet.child_mimik)
        self.assertFalse(self.parents_sheet.child_understanding)
        self.assertFalse(self.parents_sheet.child_stranger)
        self.assertFalse(self.parents_sheet.child_gestik)

    def test_crawl_age_advise_defaults_to_unbekannt(self):
        self.assertEqual(self.parents_sheet.crawl_age_advise, 'unbekannt')

    def test_child_use_of_language_defaults_to_weniger(self):
        self.assertEqual(self.parents_sheet.child_use_of_language, 'weniger')

    def test_blank_char_fields_default_to_empty_string(self):
        self.assertEqual(self.parents_sheet.health_assurance, '')
        self.assertEqual(self.parents_sheet.mother_job, '')

    def test_manager_filters_by_sheet_created(self):
        Parents_sheet.objects.create(
            child_first_name='Erika',
            child_last_name='Musterfrau',
            sheet_created=True,
        )
        open_sheets = Parents_sheet.objects.filter(sheet_created=False)
        self.assertIn(self.parents_sheet, open_sheets)
        self.assertEqual(open_sheets.count(), 1)

    def test_create_and_update_are_tracked_in_history(self):
        self.assertEqual(self.parents_sheet.history.count(), 1)
        self.assertEqual(self.parents_sheet.history.first().history_type, '+')

        self.parents_sheet.sheet_created = True
        self.parents_sheet.save()

        self.assertEqual(self.parents_sheet.history.count(), 2)
        latest, previous = self.parents_sheet.history.all()
        self.assertEqual(latest.history_type, '~')
        self.assertTrue(latest.sheet_created)
        self.assertFalse(previous.sheet_created)
