# app/predictor.py
import pandas as pd
import joblib
import streamlit as st
import os

@st.cache_resource
def load_ml_assets():
    """
    Loads and caches the trained model and preprocessors.
    Using @st.cache_resource prevents reloading these heavy files 
    every time the user moves a slider on the frontend.
    """
    try:
        # Paths relative to the app execution directory
        model = joblib.load('../models/best_model.pkl')
        preprocessor = joblib.load('../models/preprocessor.joblib')
        label_encoder = joblib.load('../models/label_encoders.pkl')
        feature_columns = joblib.load('../models/feature_columns.pkl')
        return model, preprocessor, label_encoder, feature_columns
    except Exception as e:
        st.error(f"Error loading ML assets. Please ensure models are saved correctly. Details: {e}")
        return None, None, None, None

def predict_fertilizer(input_data: dict, model, preprocessor, label_encoder) -> str:
    """
    Takes raw dictionary input from the frontend, applies the exact preprocessing 
    used during training, and returns the human-readable fertilizer prediction.
    """
    try:
        # 1. Convert input dictionary to DataFrame
        df_input = pd.DataFrame([input_data])
        
        # 2. Apply the saved ColumnTransformer (scales numerical, encodes categorical)
        X_processed = preprocessor.transform(df_input)
        
        # 3. Predict using the XGBoost model
        prediction_encoded = model.predict(X_processed)
        
        # 4. Decode the numerical prediction back to text (e.g., 0 -> 'Urea')
        predicted_fertilizer = label_encoder.inverse_transform(prediction_encoded)[0]
        
        return predicted_fertilizer
    except Exception as e:
        st.error(f"Prediction Error: {e}")
        return "Error predicting fertilizer"