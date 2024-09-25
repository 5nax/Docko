from crispy_forms.helper import FormHelper
from django import forms
import pandas as pd
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div
import pandas as pd

# Load the dataset and clean it
df = pd.read_csv('predictor/Training.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.loc[:, :'prognosis']

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'[^a-z0-9_]', '', regex=True)
    .str.replace('_+', '_', regex=True)
)

# Get symptom columns (exclude 'prognosis')
SYMPTOM_COLUMNS = df.columns[:-1]

# Create symptom choices
SYMPTOM_CHOICES = [
    (symptom, symptom.replace('_', ' ').title())
    for symptom in SYMPTOM_COLUMNS
]

from django import forms

class SymptomForm(forms.Form):
    SYMPTOM_CHOICES = [
        ('General Symptoms', [
            ('itching', 'Itching'),
            ('skin_rash', 'Skin Rash'),
            ('shivering', 'Shivering'),
            ('chills', 'Chills'),
            ('fatigue', 'Fatigue'),
            ('weight_gain', 'Weight Gain'),
            ('weight_loss', 'Weight Loss'),
            ('lethargy', 'Lethargy'),
            ('anxiety', 'Anxiety'),
            ('mood_swings', 'Mood Swings'),
            ('restlessness', 'Restlessness'),
            ('high_fever', 'High Fever'),
            ('mild_fever', 'Mild Fever'),
        ]),
        ('Gastrointestinal Symptoms', [
            ('stomach_pain', 'Stomach Pain'),
            ('acidity', 'Acidity'),
            ('ulcers_on_tongue', 'Ulcers on Tongue'),
            ('vomiting', 'Vomiting'),
            ('diarrhea', 'Diarrhea'),
            ('constipation', 'Constipation'),
            ('abdominal_pain', 'Abdominal Pain'),
            ('nausea', 'Nausea'),
            ('loss_of_appetite', 'Loss of Appetite'),
        ]),
        ('Respiratory Symptoms', [
            ('continuous_sneezing', 'Continuous Sneezing'),
            ('cough', 'Cough'),
            ('breathlessness', 'Breathlessness'),
            ('chest_pain', 'Chest Pain'),
            ('fast_heart_rate', 'Fast Heart Rate'),
            ('phlegm', 'Phlegm'),
            ('throat_irritation', 'Throat Irritation'),
            ('sinus_pressure', 'Sinus Pressure'),
            ('runny_nose', 'Runny Nose'),
            ('congestion', 'Congestion'),
        ]),
        ('Urinary Symptoms', [
            ('burning_micturition', 'Burning Micturition'),
            ('spotting_urination', 'Spotting Urination'),
            ('bladder_discomfort', 'Bladder Discomfort'),
            ('foul_smell_of_urine', 'Foul Smell of Urine'),
            ('continuous_feel_of_urine', 'Continuous Feel of Urine'),
        ]),
        ('Neurological Symptoms', [
            ('headache', 'Headache'),
            ('dizziness', 'Dizziness'),
            ('muscle_pain', 'Muscle Pain'),
            ('weakness_in_limbs', 'Weakness in Limbs'),
            ('loss_of_balance', 'Loss of Balance'),
            ('stiff_neck', 'Stiff Neck'),
            ('loss_of_smell', 'Loss of Smell'),
            ('slurred_speech', 'Slurred Speech'),
        ]),
        ('Musculoskeletal Symptoms', [
            ('joint_pain', 'Joint Pain'),
            ('muscle_wasting', 'Muscle Wasting'),
            ('muscle_weakness', 'Muscle Weakness'),
            ('neck_pain', 'Neck Pain'),
            ('swelling_joints', 'Swelling Joints'),
            ('movement_stiffness', 'Movement Stiffness'),
        ]),
        ('Skin and Nails Symptoms', [
            ('itching', 'Itching'),
            ('skin_rash', 'Skin Rash'),
            ('yellowish_skin', 'Yellowish Skin'),
            ('swelling_of_stomach', 'Swelling of Stomach'),
            ('puffy_face_and_eyes', 'Puffy Face and Eyes'),
            ('brittle_nails', 'Brittle Nails'),
            ('skin_peeling', 'Skin Peeling'),
        ]),
        ('Other Symptoms', [
            ('dehydration', 'Dehydration'),
            ('indigestion', 'Indigestion'),
            ('abnormal_menstruation', 'Abnormal Menstruation'),
            ('family_history', 'Family History'),
            ('extra_marital_contacts', 'Extra Marital Contacts'),
        ]),
    ]

    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Select your symptoms',
    )