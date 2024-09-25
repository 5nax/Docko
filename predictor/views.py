# predictor/views.py
from doctor_login.models import docDetails
from django.shortcuts import render
from .forms import SymptomForm
import joblib
import pandas as pd
from .disease_specialization import DISEASE_SPECIALIZATION

# Load the model and label encoder once when the server starts
model = joblib.load('predictor/disease_prediction_model.joblib')
le = joblib.load('predictor/label_encoder.joblib')

# Load and preprocess the dataset
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

def predict_disease(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            selected_symptoms = form.cleaned_data['symptoms']
            input_data = [0] * len(SYMPTOM_COLUMNS)
            for symptom in selected_symptoms:
                if symptom in SYMPTOM_COLUMNS:
                    index = list(SYMPTOM_COLUMNS).index(symptom)
                    input_data[index] = 1
            # Create DataFrame with standardized column names
            input_df = pd.DataFrame([input_data], columns=SYMPTOM_COLUMNS)
            prediction = model.predict(input_df)
            predicted_disease = le.inverse_transform(prediction)[0]

            # Get the specialization
            specialization = DISEASE_SPECIALIZATION.get(predicted_disease, None)

            # Query doctors with the specialization
            recommended_doctors = None
            if specialization:
                recommended_doctors = docDetails.objects.filter(specialization__icontains=specialization)

            context = {
                'form': form,
                'predicted_disease': predicted_disease,
                'recommended_doctors': recommended_doctors,
            }
            return render(request, 'predictor/result.html', context)
    else:
        form = SymptomForm()
    return render(request, 'predictor/predict.html', {'form': form})
