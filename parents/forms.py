from django import forms

from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML, Hidden
from django.utils.safestring import mark_safe

from parents.models import Parents_sheet


class ParentsSheetFormStep1(ModelForm):
    child_last_name = forms.CharField(label="Name", required=True)
    child_first_name = forms.CharField(label="Vorname", required=True)
    child_day_of_birth = forms.DateField(label="Geburtsdatum", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    health_assurance = forms.CharField(label="Krankenkasse", required=False)
    doctor = forms.CharField(label="überweisender Arzt", required=False)
    phone = forms.CharField(label="Telefon", required=False)
    cellphone = forms.CharField(label="Mobil", required=False)
    phone_work = forms.CharField(label="Dienstlich", required=False)
    email = forms.CharField(label="E-Mail", required=False)
    mother_last_name = forms.CharField(label="Name", required=False)
    mother_first_name = forms.CharField(label="Vorname", required=False)
    mother_day_of_birth = forms.DateField(label="Geburtsdatum", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    mother_job = forms.CharField(label="Beruf", required=False)
    father_last_name = forms.CharField(label="Name", required=False)
    father_first_name = forms.CharField(label="Vorname", required=False)
    father_day_of_birth = forms.DateField(label="Geburtsdatum", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    father_job = forms.CharField(label="Beruf", required=False)
    siblings1_last_name = forms.CharField(label="Name", required=False)
    siblings1_first_name = forms.CharField(label="Vorname", required=False)
    siblings1_age = forms.CharField(label="Alter", required=False)
    siblings2_last_name = forms.CharField(label="Name", required=False)
    siblings2_first_name = forms.CharField(label="Vorname", required=False)
    siblings2_age = forms.CharField(label="Alter", required=False)
    siblings3_last_name = forms.CharField(label="Name", required=False)
    siblings3_first_name = forms.CharField(label="Vorname", required=False)
    siblings3_age = forms.CharField(label="Alter", required=False)
    child_comments_1 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)

    class Meta:
        model = Parents_sheet
        fields = [
            'child_last_name',
            'child_first_name',
            'child_day_of_birth',
            'health_assurance',
            'doctor',
            'phone',
            'cellphone',
            'phone_work',
            'email',
            'mother_last_name',
            'mother_first_name',
            'mother_day_of_birth',
            'mother_job',
            'father_last_name',
            'father_first_name',
            'father_day_of_birth',
            'father_job',
            'siblings1_last_name',
            'siblings1_first_name',
            'siblings1_age',
            'siblings2_last_name',
            'siblings2_first_name',
            'siblings2_age',
            'siblings3_last_name',
            'siblings3_first_name',
            'siblings3_age',
            'child_comments_1'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),  # Formtools Hidden-Input
            HTML("<h4 class='text-center'>Angaben zum Kind:</h4>"),

            Field("child_last_name", css_class="form-control"),
            Field("child_first_name", css_class="form-control"),
            Field("child_day_of_birth", css_class="form-control"),
            Field("health_assurance", css_class="form-control"),
            Field("doctor", css_class="form-control"),
            Field("phone", css_class="form-control"),
            Field("email", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zur Mutter:</h4>"),
            Field("mother_last_name", css_class="form-control"),
            Field("mother_first_name", css_class="form-control"),
            Field("mother_day_of_birth", css_class="form-control"),
            Field("mother_job", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zum Vater</h4>"),
            Field("father_last_name", css_class="form-control"),
            Field("father_first_name", css_class="form-control"),
            Field("father_day_of_birth", css_class="form-control"),
            Field("father_job", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zu den Geschwistern:</h4>"),
            HTML("<h5 class='text-center'>Erstes Geschwisterkind:</h5>"),
            Field("siblings1_last_name", css_class="form-control"),
            Field("siblings1_first_name", css_class="form-control"),
            Field("siblings1_age", css_class="form-control"),
            HTML("<h5 class='text-center'>Zweites Geschwisterkind:</h5>"),
            Field("siblings2_last_name", css_class="form-control"),
            Field("siblings2_first_name", css_class="form-control"),
            Field("siblings2_age", css_class="form-control"),
            HTML("<h5 class='text-center'>Drittes Geschwisterkind:</h5>"),
            Field("siblings3_last_name", css_class="form-control"),
            Field("siblings3_first_name", css_class="form-control"),
            Field("siblings3_age", css_class="form-control"),
        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_1", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetFormStep2(ModelForm):

    problems_pregnancy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-problems_pregnancy_yes'
                                               }),
                                           label="Gab es Schwierigkeiten bei der Schwangerschaft/Geburt?",
                                           required=False)
    problems_pregnancy_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    problems_family_speak_listen = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                     widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-problems_family_speak_listen_yes'
                                               }),
                                                     label="Hat oder hatte jemand in der Familie (Verwandschaft) Schwierigkeiten mit dem Sprechen oder Hören?",
                                                     required=False)
    problems_family_speak_listen_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_allergy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-child_allergy_yes'
                                               }),
                                      label="Hat ihr Kind eine Allergie?",
                                      required=False)

    child_allergy_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    crawl_age = forms.CharField(label="Ab welchem Lebensmonat hat das Kind gekrabbelt?", required=False)

    crawl_age_advise = forms.ChoiceField(choices=Parents_sheet.AGEADVICE_CHOICES,
                                         label="verspätet oder altersgerecht?",
                                         required=False)

    walk_age = forms.CharField(label="Ab welchem Lebensmonat hat das Kind gelaufen?", required=False)

    walk_age_advise = forms.ChoiceField(choices=Parents_sheet.AGEADVICE_CHOICES,
                                        label="verspätet oder altersgerecht?",
                                        required=False)

    child_dev_1 = forms.CharField(label="Wann war das Kind sauber?", required=False)
    child_dev_2 = forms.CharField(label="Erste Lall-Laute (erre, grr, äää)", required=False)
    child_dev_3 = forms.CharField(label="Erste Worte (Mama, Ball, ...)", required=False)
    child_dev_4 = forms.CharField(label="Erste Zwei-Wort-Sätze", required=False)

    child_dev_language = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-child_dev_language_yes'
                                               }),
                                           label="Wächst ihr Kind mehrsprachig auf (auch Dialekte)?",
                                           required=False)
    child_dev_language_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_dev_5 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                    widget=forms.RadioSelect(),
                                    label="Hat/Hatte Ihr Kind Lutschgewohnheiten (Daumen, Schnuller, Finger ... u.s.w.)?",
                                    required=False)

    child_left_handed = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                          widget=forms.RadioSelect(),
                                          label="Ist Ihr Kind Linkshänder/in?",
                                          required=False)

    child_comments_2 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)

    class Meta:
        model = Parents_sheet
        fields = [
            'problems_pregnancy',
            'problems_pregnancy_yes',
            'problems_family_speak_listen',
            'problems_family_speak_listen_yes',
            'child_allergy',
            'child_allergy_yes',
            'crawl_age',
            'crawl_age_advise',
            'walk_age',
            'walk_age_advise',
            'child_dev_1',
            'child_dev_2',
            'child_dev_3',
            'child_dev_4',
            'child_dev_language',
            'child_dev_language_yes',
            'child_dev_5',
            'child_left_handed',
            'child_comments_2'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),
            HTML("<div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div><br>"),

            HTML("<h4 class='text-center'>Allgemeine Entwicklung des Kindes:</h4><br>"),
            Field("problems_pregnancy", css_class="custom-radio"),
            Field("problems_pregnancy_yes", css_class="form-control"),
            Field("problems_family_speak_listen", css_class="custom-radio"),
            Field("problems_family_speak_listen_yes", css_class="form-control"),
            Field("child_allergy", css_class="custom-radio"),
            Field("child_allergy_yes", css_class="form-control"),
            Field("crawl_age", css_class="form-control"),
            Field("crawl_age_advise", css_class="custom-radio"),
            Field("walk_age", css_class="form-control"),
            Field("walk_age_advise", css_class="custom-radio"),
            Field("child_dev_1", css_class="form-control"),
            Field("child_dev_2", css_class="form-control"),
            Field("child_dev_3", css_class="form-control"),
            Field("child_dev_4", css_class="form-control"),
            Field("child_dev_language", css_class="custom-radio"),
            Field("child_dev_language_yes", css_class="form-control"),
            Field("child_dev_5", css_class="custom-radio"),
            Field("child_left_handed", css_class="custom-radio"),
        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_2", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetFormStep3(ModelForm):
    child_chronic_disease = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                              widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_chronic_disease_yes'
                                               }),
                                              label="Liegt eine chronische Erkrankung oder eine Behinderung vor?",
                                              required=False)
    child_chronic_disease_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_nutrition = forms.CharField(label="Wie ist die Ernährung? (vom Stillen bis heute)", required=False)

    child_hospital_visits = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_hospital_visits_yes'
                                               }),
                                              label="Krankenhausaufenthalte (Mandeln/Polypen, ...)?",
                                              required=False)
    child_hospital_visits_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_medicine = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_medicine_yes'
                                               }),
                                       label="Nimmt ihr Kind Medikamente?",
                                       required=False)
    child_medicine_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_count_colds = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect,
                                          label="Ist Ihr Kind häufiger als 3 mal im Jahr erkältet?",
                                          required=False)

    child_timpani_tube = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect,
                                           label="Hat Ihr Kind Paukenröhrchen?",
                                           required=False)

    child_listen = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Haben Sie das Gefühl, dass Ihr Kind phasenweise schlecht hört?",
                                     required=False)

    child_illness_1 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                        widget=forms.RadioSelect,
                                        label="Hatte Ihr Kind bisher mehr als 3 Mittelohrentzündungen?",
                                        required=False)

    child_illness_2 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                        widget=forms.RadioSelect,
                                        label="Ist Ihr Kind Mundatmer und / oder schnarcht es?",
                                        required=False)

    child_what_teething = forms.CharField(label="Welche Kinderkrankheiten hatte Ihr Kind?", required=False)

    child_comments_3 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)
    class Meta:
        model = Parents_sheet
        fields = [
            'child_chronic_disease',
            'child_chronic_disease_yes',
            'child_nutrition',
            'child_hospital_visits',
            'child_hospital_visits_yes',
            'child_medicine',
            'child_medicine_yes',
            'child_count_colds',
            'child_timpani_tube',
            'child_listen',
            'child_illness_1',
            'child_illness_2',
            'child_what_teething',
            'child_comments_3'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),
            HTML("<div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div><br>"),

            HTML("<h4 class='text-center'>Erkrankungen des Kindes:</h4><br>"),
            Field("child_chronic_disease", css_class="custom-radio"),
            Field("child_chronic_disease_yes", css_class="form-control"),
            Field("child_nutrition", css_class="form-control"),
            Field("child_hospital_visits", css_class="custom-radio"),
            Field("child_hospital_visits_yes", css_class="form-control"),
            Field("child_medicine", css_class="custom-radio"),
            Field("child_medicine_yes", css_class="form-control"),
            Field("child_count_colds", css_class="custom-radio"),
            Field("child_timpani_tube", css_class="custom-radio"),
            Field("child_listen", css_class="custom-radio"),
            Field("child_illness_1", css_class="custom-radio"),
            Field("child_illness_2", css_class="custom-radio"),
            Field("child_what_teething", css_class="form-control"),

        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_3", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetFormStep4(ModelForm):
    child_glases = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Trägt Ihr Kind ständig eine Brille oder nur beim Lesen?",
                                     required=False)

    child_hearing_aid = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                          widget=forms.RadioSelect,
                                          label="Trägt Ihr Kind ein Hörgerät oder ist eines vorgesehen?",
                                          required=False)

    child_problems_sleeping_hearing = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                        widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_3-child_problems_sleeping_hearing_yes'
                                               }),
                                                        label="Gibt es Schwierigkeiten in Bezug auf Sprache, Hören, Schlafen, Fernsehen?",
                                                        required=False)
    child_problems_sleeping_hearing_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_use_of_language = forms.ChoiceField(choices=Parents_sheet.LANGUAGEUSE_CHOICES,
                                              label="Wie schätzen Sie den Sprachgebrauch Ihres Kindes während seiner Sprachentwicklung ein? Es hat eher: (viel, weniger, kaum, gar nicht) gesprochen", required=False)

    child_speaking_interrupt = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                 widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_3-child_speaking_interrupt_yes'
                                               }),
                                                 label="Hat Ihr Kind zwar zu sprechen begonnen, dann aber damit plötzlich aufgehört?",
                                                 required=False)
    child_speaking_interrupt_yes = forms.CharField(label="Wenn ja, wann?", required=False)

    child_speaking_dev = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_3-child_speaking_dev_yes'
                                               }),
                                           label="Hat sich die Sprache Ihres Kindes ab einem bestimmten Zeitpunkt nicht mehr weiterentwickelt?",
                                           required=False)
    child_speaking_dev_yes = forms.CharField(label="Wenn ja, wann?", required=False)

    child_mimik = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                    widget=forms.RadioSelect,
                                    label="Müssen Sie Ihre Äußerungen durch Mimik und Gesten unterstützen, damit Ihr Kind Sie versteht?",
                                    required=False)

    child_understanding = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Fällt es Ihnen und nahestehenden Personen schwer, ihr Kind zu verstehen?",
                                            required=False)

    child_stranger = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Fällt es Fremden schwer, ihr Kind zu verstehen?",
                                            required=False)

    child_gestik = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Verständigt sich Ihr Kind hauptsächlich durch Gestik und Mimik?",
                                            required=False)

    child_letter_wrong = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_3-child_letter_wrong_yes'
                                               }),
                                           label="Bildet Ihr Kind bestimmte Buchstaben falsch?",
                                           required=False)
    child_letter_wrong_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_sentence_construction = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                    widget=forms.RadioSelect,
                                                    label="Erscheint Ihnen der Satzbau Ihres Kindes, im Vergleich zu anderen gleichaltrigen Kindern, auffällig?",
                                                    required=False)

    child_speech = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Ist die Stimme Ihres Kindes auffällig (rauh, heißer, ...)?",
                                     required=False)

    child_noises_reaktion = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                              widget=forms.RadioSelect,
                                              label="Hat Ihr Kind Probleme, auf alltägliche Geräusche (z.B. Türklingel, Telefon, Kaffeemaschine) zu reagieren, v.a. wenn diese nicht in unmittelbarer Nähe sind?",
                                              required=False)

    child_watch_contact = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Benötigt Ihr Kind Blickkontakt, um auf Ihre Ansprache reagieren zu können?",
                                            required=False)

    child_talking = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                      label="Überschlägt sich Ihr Kind beim Sprechen? Lässt es Wörter oder Satzteile aus?",
                                      required=False)

    child_stutter = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                      label="Haben Sie den Eindruck, dass Ihr Kind stottert?",
                                      required=False)

    child_comments_4 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)
    class Meta:
        model = Parents_sheet
        fields = [
            'child_glases',
            'child_hearing_aid',
            'child_problems_sleeping_hearing',
            'child_problems_sleeping_hearing_yes',
            'child_use_of_language',
            'child_speaking_interrupt',
            'child_speaking_interrupt_yes',
            'child_speaking_dev',
            'child_speaking_dev_yes',
            'child_mimik',
            'child_understanding',
            'child_stranger',
            'child_gestik',
            'child_letter_wrong',
            'child_letter_wrong_yes',
            'child_sentence_construction',
            'child_speech',
            'child_noises_reaktion',
            'child_watch_contact',
            'child_talking',
            'child_stutter',
            'child_comments_4'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),
            HTML("<div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div><br>"),

            HTML("<h4 class='text-center'>Hören, Sprechen, Verstehen:</h4><br>"),

            Field("child_glases", css_class="custom-radio"),
            Field("child_hearing_aid", css_class="custom-radio"),
            Field("child_problems_sleeping_hearing", css_class="custom-radio"),
            Field("child_problems_sleeping_hearing_yes", css_class="form-control"),
            Field("child_use_of_language", css_class="form-control"),
            Field("child_speaking_interrupt", css_class="custom-radio"),
            Field("child_speaking_interrupt_yes", css_class="form-control"),
            Field("child_speaking_dev", css_class="custom-radio"),
            Field("child_speaking_dev_yes", css_class="form-control"),
            Field("child_mimik", css_class="custom-radio"),
            Field("child_understanding", css_class="custom-radio"),
            Field("child_stranger", css_class="custom-radio"),
            Field("child_gestik", css_class="custom-radio"),
            Field("child_letter_wrong", css_class="custom-radio"),
            Field("child_letter_wrong_yes", css_class="form-control"),
            Field("child_sentence_construction", css_class="custom-radio"),
            Field("child_speech", css_class="custom-radio"),
            Field("child_noises_reaktion", css_class="custom-radio"),
            Field("child_watch_contact", css_class="custom-radio"),
            Field("child_talking", css_class="custom-radio"),
            Field("child_stutter", css_class="custom-radio"),

        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_4", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetFormStep5(ModelForm):
    child_development = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                          label="Ist die allgemeine Entwicklung altersgerecht (Selbstständigkeit, Konzentration, ...)?", required=False)
    child_playing_1 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                         label="Spielt es gerne mit anderen Kindern?", required=False)
    child_playing_2 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                         label="Spielt es auch alleine?", required=False)
    child_playing_3 = forms.CharField(label="Womit spielt es gerne?", required=False)

    child_school = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_4-child_school_yes, div_id_4-child_school_which'
                                               }),
                                      label="Geht Ihr Kind in den Kindergarten / in die Schule?", required=False)
    child_school_yes = forms.CharField(label="Wenn ja, seit wann?", required=False)

    child_school_which = forms.CharField(label="in welche(n)?", required=False)

    child_comments_5 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)
    class Meta:
        model = Parents_sheet
        fields = [
            'child_development',
            'child_playing_1',
            'child_playing_2',
            'child_playing_3',
            'child_school',
            'child_school_yes',
            'child_school_which',
            'child_comments_5'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),
            HTML("<div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div><br>"),

            HTML("<h4 class='text-center'>Spielerische und schulische Entwicklung des Kindes:</h4><br>"),

            Field("child_development", css_class="custom-radio"),
            Field("child_playing_1", css_class="custom-radio"),
            Field("child_playing_2", css_class="custom-radio"),
            Field("child_playing_3", css_class="form-control"),
            Field("child_school", css_class="custom-radio"),
            Field("child_school_yes", css_class="form-control"),
            Field("child_school_which", css_class="form-control"),

        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_5", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-primary'>Weiter</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetFormStep6(ModelForm):
    child_caregivers = forms.CharField(label="Welche Bezugspersonen hat Ihr Kind hauptsächlich? (Erziehungssituation)", required=False)

    child_speech_therapy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                             widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_5-child_speech_therapy_yes'
                                               }),
                                             label="War oder ist Ihr Kind in logopädischer Behandlung? (sonstige Behandlungen)",
                                             required=False)

    child_speech_therapy_yes = forms.CharField(label="Wenn ja, bei wem? (Nennen Sie Zeitraum und Anzahl der Therapiestunden)", required=False)

    child_speech_therapy_advise = forms.CharField(widget=forms.Textarea,
                                                  label="Beschreiben Sie, warum Sie logopädischen Rat einholen möchten? (persönliche Beweggründe)",
                                                  required=False)

    child_comments_6 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin</strong>"),
                                       required=False)

    class Meta:
        model = Parents_sheet
        fields = [
            'child_caregivers',
            'child_speech_therapy',
            'child_speech_therapy_yes',
            'child_speech_therapy_advise',
            'child_comments_6'
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("{{ wizard.management_form }}"),
            Hidden("wizard_step", "{{ wizard.steps.step1 }}"),
            HTML("<div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-warning'>Final absenden</button></div><br>"),
            HTML("<h4 class='text-center'>Fragen zur logopädischen Behandlung:</h4><br>"),

            Field("child_caregivers", css_class="form-control"),
            Field("child_speech_therapy", css_class="custom-radio"),
            Field("child_speech_therapy_yes", css_class="form-control"),
            Field("child_speech_therapy_advise", css_class="form-control"),

        ]

        if user and user.is_authenticated:
            layout_fields.append(Field("child_comments_6", css_class="form-control"))

        layout_fields.append(
            HTML("<br><div class='button-group'>"
                 "{% if wizard.steps.prev %}"
                 "<button type='submit' name='wizard_goto_step' value='{{ wizard.steps.prev }}' class='btn btn-primary'>Zurück</button>&nbsp;"
                 "{% endif %}"
                 "<button type='submit' class='btn btn-warning'>Final absenden</button></div>")
        )

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetForm(ModelForm):
    child_last_name = forms.CharField(label="Name", required=True)
    child_first_name = forms.CharField(label="Vorname", required=True)
    child_day_of_birth = forms.DateField(label="Geburtsdatum", required=False)
    health_assurance = forms.CharField(label="Krankenkasse", required=False)
    doctor = forms.CharField(label="überweisender Arzt", required=False)
    phone = forms.CharField(label="Telefon", required=False)
    cellphone = forms.CharField(label="Mobil", required=False)
    phone_work = forms.CharField(label="Dienstlich", required=False)
    email = forms.CharField(label="E-Mail", required=False)
    mother_last_name = forms.CharField(label="Name", required=False)
    mother_first_name = forms.CharField(label="Vorname", required=False)
    mother_day_of_birth = forms.DateField(label="Geburtsdatum", required=False)
    mother_job = forms.CharField(label="Beruf", required=False)
    father_last_name = forms.CharField(label="Name", required=False)
    father_first_name = forms.CharField(label="Vorname", required=False)
    father_day_of_birth = forms.DateField(label="Geburtsdatum", required=False)
    father_job = forms.CharField(label="Beruf", required=False)
    siblings1_last_name = forms.CharField(label="Name", required=False)
    siblings1_first_name = forms.CharField(label="Vorname", required=False)
    siblings1_age = forms.CharField(label="Alter", required=False)
    siblings2_last_name = forms.CharField(label="Name", required=False)
    siblings2_first_name = forms.CharField(label="Vorname", required=False)
    siblings2_age = forms.CharField(label="Alter", required=False)
    siblings3_last_name = forms.CharField(label="Name", required=False)
    siblings3_first_name = forms.CharField(label="Vorname", required=False)
    siblings3_age = forms.CharField(label="Alter", required=False)
    child_comments_1 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 1)</strong>"),
                                       required=False)

    problems_pregnancy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-problems_pregnancy_yes'
                                               }),
                                           label="Gab es Schwierigkeiten bei der Schwangerschaft/Geburt?",
                                           required=False)
    problems_pregnancy_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    problems_family_speak_listen = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                     widget=forms.RadioSelect(attrs={
                                                        'data-target': 'div_id_1-problems_family_speak_listen_yes'
                                                     }),
                                                     label="Hat oder hatte jemand in der Familie (Verwandschaft) Schwierigkeiten mit dem Sprechen oder Hören?",
                                                     required=False)
    problems_family_speak_listen_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_allergy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-child_allergy_yes'
                                               }),
                                      label="Hat ihr Kind eine Allergie?",
                                      required=False)
    child_allergy_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    crawl_age = forms.CharField(label="Ab welchem Lebensmonat hat das Kind gekrabbelt?", required=False)
    crawl_age_advise = forms.ChoiceField(choices=Parents_sheet.AGEADVICE_CHOICES,
                                         label="verspätet oder altersgerecht?",
                                         required=False)

    walk_age = forms.CharField(label="Ab welchem Lebensmonat hat das Kind gelaufen?", required=False)

    walk_age_advise = forms.ChoiceField(choices=Parents_sheet.AGEADVICE_CHOICES,
                                        label="verspätet oder altersgerecht?",
                                        required=False)

    child_dev_1 = forms.CharField(label="Wann war das Kind sauber?", required=False)
    child_dev_2 = forms.CharField(label="Erste Lall-Laute (erre, grr, äää)", required=False)
    child_dev_3 = forms.CharField(label="Erste Worte (Mama, Ball, ...)", required=False)
    child_dev_4 = forms.CharField(label="Erste Zwei-Wort-Sätze", required=False)

    child_dev_language = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_1-child_dev_language_yes'
                                               }),
                                           label="Wächst ihr Kind mehrsprachig auf (auch Dialekte)?",
                                           required=False)
    child_dev_language_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_dev_5 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                    widget=forms.RadioSelect(),
                                    label="Hat/Hatte Ihr Kind Lutschgewohnheiten (Daumen, Schnuller, Finger ... u.s.w.)?",
                                    required=False)

    child_left_handed = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                          widget=forms.RadioSelect(),
                                          label="Ist Ihr Kind Linkshänder/in?",
                                          required=False)

    child_comments_2 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 2)</strong>"),
                                       required=False)

    child_chronic_disease = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                              widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_chronic_disease_yes'
                                               }),
                                              label="Liegt eine chronische Erkrankung oder eine Behinderung vor?",
                                              required=False)
    child_chronic_disease_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_nutrition = forms.CharField(label="Wie ist die Ernährung? (vom Stillen bis heute)", required=False)

    child_hospital_visits = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_hospital_visits_yes'
                                               }),
                                              label="Krankenhausaufenthalte (Mandeln/Polypen, ...)?",
                                              required=False)
    child_hospital_visits_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_medicine = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_2-child_medicine_yes'
                                               }),
                                       label="Nimmt ihr Kind Medikamente?",
                                       required=False)
    child_medicine_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_count_colds = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect,
                                          label="Ist Ihr Kind häufiger als 3 mal im Jahr erkältet?",
                                          required=False)

    child_timpani_tube = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect,
                                           label="Hat Ihr Kind Paukenröhrchen?",
                                           required=False)

    child_listen = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Haben Sie das Gefühl, dass Ihr Kind phasenweise schlecht hört?",
                                     required=False)

    child_illness_1 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                        widget=forms.RadioSelect,
                                        label="Hatte Ihr Kind bisher mehr als 3 Mittelohrentzündungen?",
                                        required=False)

    child_illness_2 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                        widget=forms.RadioSelect,
                                        label="Ist Ihr Kind Mundatmer und / oder schnarcht es?",
                                        required=False)

    child_what_teething = forms.CharField(label="Welche Kinderkrankheiten hatte Ihr Kind?", required=False)

    child_comments_3 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 3)</strong>"),
                                       required=False)

    child_glases = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Trägt Ihr Kind ständig eine Brille oder nur beim Lesen?",
                                     required=False)

    child_hearing_aid = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                          widget=forms.RadioSelect,
                                          label="Trägt Ihr Kind ein Hörgerät oder ist eines vorgesehen?",
                                          required=False)

    child_problems_sleeping_hearing = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                        widget=forms.RadioSelect(attrs={
                                                            'data-target': 'div_id_3-child_problems_sleeping_hearing_yes'
                                                        }),
                                                        label="Gibt es Schwierigkeiten in Bezug auf Sprache, Hören, Schlafen, Fernsehen?",
                                                        required=False)
    child_problems_sleeping_hearing_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_use_of_language = forms.ChoiceField(choices=Parents_sheet.LANGUAGEUSE_CHOICES,
        label="Wie schätzen Sie den Sprachgebrauch Ihres Kindes während seiner Sprachentwicklung ein? Es hat eher: (viel, weniger, kaum, gar nicht) gesprochen",
        required=False)

    child_speaking_interrupt = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                 widget=forms.RadioSelect(attrs={
                                                     'data-target': 'div_id_3-child_speaking_interrupt_yes'
                                                 }),
                                                 label="Hat Ihr Kind zwar zu sprechen begonnen, dann aber damit plötzlich aufgehört?",
                                                 required=False)
    child_speaking_interrupt_yes = forms.CharField(label="Wenn ja, wann?", required=False)

    child_speaking_dev = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                               'data-target': 'div_id_3-child_speaking_dev_yes'
                                           }),
                                           label="Hat sich die Sprache Ihres Kindes ab einem bestimmten Zeitpunkt nicht mehr weiterentwickelt?",
                                           required=False)
    child_speaking_dev_yes = forms.CharField(label="Wenn ja, wann?", required=False)

    child_mimik = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                    widget=forms.RadioSelect,
                                    label="Müssen Sie Ihre Äußerungen durch Mimik und Gesten unterstützen, damit Ihr Kind Sie versteht?",
                                    required=False)

    child_understanding = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Fällt es Ihnen und nahestehenden Personen schwer, ihr Kind zu verstehen?",
                                            required=False)

    child_stranger = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Fällt es Fremden schwer, ihr Kind zu verstehen?",
                                            required=False)

    child_gestik = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Verständigt sich Ihr Kind hauptsächlich durch Gestik und Mimik?",
                                            required=False)

    child_letter_wrong = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                           widget=forms.RadioSelect(attrs={
                                               'data-target': 'div_id_3-child_letter_wrong_yes'
                                           }),
                                           label="Bildet Ihr Kind bestimmte Buchstaben falsch?",
                                           required=False)
    child_letter_wrong_yes = forms.CharField(label="Wenn ja, welche?", required=False)

    child_sentence_construction = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                                    widget=forms.RadioSelect,
                                                    label="Erscheint Ihnen der Satzbau Ihres Kindes, im Vergleich zu anderen gleichaltrigen Kindern, auffällig?",
                                                    required=False)

    child_speech = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                     widget=forms.RadioSelect,
                                     label="Ist die Stimme Ihres Kindes auffällig (rauh, heißer, ...)?",
                                     required=False)

    child_noises_reaktion = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                              widget=forms.RadioSelect,
                                              label="Hat Ihr Kind Probleme, auf alltägliche Geräusche (z.B. Türklingel, Telefon, Kaffeemaschine) zu reagieren, v.a. wenn diese nicht in unmittelbarer Nähe sind?",
                                              required=False)

    child_watch_contact = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                            widget=forms.RadioSelect,
                                            label="Benötigt Ihr Kind Blickkontakt, um auf Ihre Ansprache reagieren zu können?",
                                            required=False)

    child_talking = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                      label="Überschlägt sich Ihr Kind beim Sprechen? Lässt es Wörter oder Satzteile aus?",
                                      required=False)

    child_stutter = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                      label="Haben Sie den Eindruck, dass Ihr Kind stottert?",
                                      required=False)

    child_comments_4 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 4)</strong>"),
                                       required=False)

    child_development = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                          label="Ist die allgemeine Entwicklung altersgerecht (Selbstständigkeit, Konzentration, ...)?", required=False)
    child_playing_1 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                         label="Spielt es gerne mit anderen Kindern?", required=False)
    child_playing_2 = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect,
                                         label="Spielt es auch alleine?", required=False)
    child_playing_3 = forms.CharField(label="Womit spielt es gerne?", required=False)

    child_school = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                      widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_4-child_school_yes, div_id_4-child_school_which'
                                               }),
                                      label="Geht Ihr Kind in den Kindergarten / in die Schule?", required=False)
    child_school_yes = forms.CharField(label="Wenn ja, seit wann?", required=False)

    child_school_which = forms.CharField(label="in welche(n)?", required=False)

    child_comments_5 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 5)</strong>"),
                                       required=False)

    child_caregivers = forms.CharField(label="Welche Bezugspersonen hat Ihr Kind hauptsächlich? (Erziehungssituation)", required=False)

    child_speech_therapy = forms.ChoiceField(choices=[(True, "Ja"), (False, "Nein")],
                                             widget=forms.RadioSelect(attrs={
                                                   'data-target': 'div_id_5-child_speech_therapy_yes'
                                               }),
                                             label="War oder ist Ihr Kind in logopädischer Behandlung? (sonstige Behandlungen)",
                                             required=False)

    child_speech_therapy_yes = forms.CharField(label="Wenn ja, bei wem? (Nennen Sie Zeitraum und Anzahl der Therapiestunden)", required=False)

    child_speech_therapy_advise = forms.CharField(widget=forms.Textarea,
                                                  label="Beschreiben Sie, warum Sie logopädischen Rat einholen möchten? (persönliche Beweggründe)",
                                                  required=False)

    child_comments_6 = forms.CharField(widget=forms.Textarea(),
                                       label=mark_safe("<strong>Anmerkungen der Therapeutin (Themenblock 6)</strong>"),
                                       required=False)

    class Meta:
        model = Parents_sheet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        layout_fields = [
            HTML("<h4 class='text-center'>Angaben zum Kind:</h4>"),

            Field("child_last_name", css_class="form-control"),
            Field("child_first_name", css_class="form-control"),
            Field("child_day_of_birth", css_class="form-control"),
            Field("health_assurance", css_class="form-control"),
            Field("doctor", css_class="form-control"),
            Field("phone", css_class="form-control"),
            Field("cellphone", css_class="form-control"),
            Field("phone_work", css_class="form-control"),
            Field("email", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zur Mutter:</h4>"),
            Field("mother_last_name", css_class="form-control"),
            Field("mother_first_name", css_class="form-control"),
            Field("mother_day_of_birth", css_class="form-control"),
            Field("mother_job", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zum Vater</h4>"),
            Field("father_last_name", css_class="form-control"),
            Field("father_first_name", css_class="form-control"),
            Field("father_day_of_birth", css_class="form-control"),
            Field("father_job", css_class="form-control"),

            HTML("<h4 class='text-center'>Angaben zu den Geschwistern:</h4>"),

            HTML("<h5 class='text-center'>Erstes Geschwisterkind:</h5>"),
            Field("siblings1_last_name", css_class="form-control"),
            Field("siblings1_first_name", css_class="form-control"),
            Field("siblings1_age", css_class="form-control"),

            HTML("<h5 class='text-center'>Zweites Geschwisterkind:</h5>"),
            Field("siblings2_last_name", css_class="form-control"),
            Field("siblings2_first_name", css_class="form-control"),
            Field("siblings2_age", css_class="form-control"),

            HTML("<h5 class='text-center'>Drittes Geschwisterkind:</h5>"),
            Field("siblings3_last_name", css_class="form-control"),
            Field("siblings3_first_name", css_class="form-control"),
            Field("siblings3_age", css_class="form-control"),
            Field("child_comments_1", css_class="form-control"),

            HTML("<h4 class='text-center'>Allgemeine Entwicklung des Kindes:</h4><br>"),
            Field("problems_pregnancy", css_class="custom-radio"),
            Field("problems_pregnancy_yes", css_class="form-control"),
            Field("problems_family_speak_listen", css_class="custom-radio"),
            Field("problems_family_speak_listen_yes", css_class="form-control"),
            Field("child_allergy", css_class="custom-radio"),
            Field("child_allergy_yes", css_class="custom-radio"),
            Field("crawl_age", css_class="form-control"),
            Field("crawl_age_advise", css_class="form-control"),
            Field("walk_age", css_class="form-control"),
            Field("walk_age_advise", css_class="form-control"),
            Field("child_dev_1", css_class="form-control"),
            Field("child_dev_2", css_class="form-control"),
            Field("child_dev_3", css_class="form-control"),
            Field("child_dev_4", css_class="form-control"),
            Field("child_dev_language", css_class="custom-radio"),
            Field("child_dev_language_yes", css_class="form-control"),
            Field("child_dev_5", css_class="custom-radio"),
            Field("child_left_handed", css_class="custom-radio"),
            Field("child_comments_2", css_class="form-control"),

            HTML("<h4 class='text-center'>Erkrankungen des Kindes:</h4><br>"),
            Field("child_chronic_disease", css_class="custom-radio"),
            Field("child_chronic_disease_yes", css_class="form-control"),
            Field("child_nutrition", css_class="form-control"),
            Field("child_hospital_visits", css_class="custom-radio"),
            Field("child_hospital_visits_yes", css_class="form-control"),
            Field("child_medicine", css_class="custom-radio"),
            Field("child_medicine_yes", css_class="form-control"),
            Field("child_count_colds", css_class="custom-radio"),
            Field("child_timpani_tube", css_class="custom-radio"),
            Field("child_listen", css_class="custom-radio"),
            Field("child_illness_1", css_class="custom-radio"),
            Field("child_illness_2", css_class="custom-radio"),
            Field("child_what_teething", css_class="form-control"),
            Field("child_comments_3", css_class="form-control"),

            HTML("<h4 class='text-center'>Hören, Sprechen, Verstehen:</h4><br>"),
            Field("child_glases", css_class="custom-radio"),
            Field("child_hearing_aid", css_class="custom-radio"),
            Field("child_problems_sleeping_hearing", css_class="custom-radio"),
            Field("child_problems_sleeping_hearing_yes", css_class="form-control"),
            Field("child_use_of_language", css_class="form-control"),
            Field("child_speaking_interrupt", css_class="custom-radio"),
            Field("child_speaking_interrupt_yes", css_class="form-control"),
            Field("child_speaking_dev", css_class="custom-radio"),
            Field("child_speaking_dev_yes", css_class="form-control"),
            Field("child_mimik", css_class="custom-radio"),
            Field("child_understanding", css_class="custom-radio"),
            Field("child_stranger", css_class="custom-radio"),
            Field("child_gestik", css_class="custom-radio"),
            Field("child_letter_wrong", css_class="custom-radio"),
            Field("child_letter_wrong_yes", css_class="form-control"),
            Field("child_sentence_construction", css_class="custom-radio"),
            Field("child_speech", css_class="custom-radio"),
            Field("child_noises_reaktion", css_class="custom-radio"),
            Field("child_watch_contact", css_class="custom-radio"),
            Field("child_talking", css_class="custom-radio"),
            Field("child_stutter", css_class="custom-radio"),
            Field("child_comments_4", css_class="form-control"),

            HTML("<h4 class='text-center'>Spielerische und schulische Entwicklung des Kindes:</h4><br>"),
            Field("child_development", css_class="custom-radio"),
            Field("child_playing_1", css_class="custom-radio"),
            Field("child_playing_2", css_class="custom-radio"),
            Field("child_playing_3", css_class="form-control"),
            Field("child_school", css_class="custom-radio"),
            Field("child_school_yes", css_class="form-control"),
            Field("child_school_which", css_class="form-control"),
            Field("child_comments_5", css_class="form-control"),

            HTML("<h4 class='text-center'>Fragen zur logopädischen Behandlung:</h4><br>"),
            Field("child_caregivers", css_class="form-control"),
            Field("child_speech_therapy", css_class="custom-radio"),
            Field("child_speech_therapy_yes", css_class="form-control"),
            Field("child_speech_therapy_advise", css_class="form-control"),
            Field("child_comments_6", css_class="form-control"),

            HTML("<br><div><button type='submit' class='btn btn-primary'>Final absenden</button></div>")

        ]

        self.helper.layout = Layout(
            *layout_fields,
        )


class ParentsSheetListForm(forms.Form):
    patientId = forms.IntegerField(required=True,
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'autocomplete': 'off',
                                        'placeholder': 'Pat.ID'
                                    }
                                )
                                )

