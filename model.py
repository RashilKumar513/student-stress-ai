import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

@st.cache_resource
def load_model():
    df = pd.read_csv("training_data.csv")
    X = df.drop("stress_level", axis=1)
    y = df["stress_level"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    return model, scaler

def predict_stress(features):
    model, scaler = load_model()
    return int(model.predict(scaler.transform([features]))[0])
