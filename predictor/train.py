# predictor/train_model.py

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import GradientBoostingClassifier
import joblib

# Load the dataset
df = pd.read_csv('Training.csv')

# Remove any unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Ensure 'prognosis' is the target variable
# and remove any extra columns beyond it
if 'prognosis' in df.columns:
    df = df.loc[:, :'prognosis']
else:
    raise ValueError("The 'prognosis' column is missing from the dataset.")

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.replace(r'[^a-z0-9_]', '', regex=True)
    .str.replace('_+', '_', regex=True)
)

# Encode the target variable
le = LabelEncoder()
df['prognosis'] = le.fit_transform(df['prognosis'])

# Separate features and target
X = df.drop('prognosis', axis=1)
y = df['prognosis']

# Train the model
# Train the model
model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
model.fit(X, y)

# Save the model and label encoder
joblib.dump(model, 'disease_prediction_model.joblib')
joblib.dump(le, 'label_encoder.joblib')
