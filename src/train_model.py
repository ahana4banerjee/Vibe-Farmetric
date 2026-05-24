# src/train_model.py
import numpy as np
import joblib
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report
from utils import evaluate_model, plot_confusion_matrix, plot_model_comparison

def main():
    print("Loading preprocessed data...")
    # 1. Load the data created in Step 1
    X_train = np.load('../data/X_train.npy')
    X_test = np.load('../data/X_test.npy')
    y_train = np.load('../data/y_train.npy')
    y_test = np.load('../data/y_test.npy')
    
    # Load label encoder to get actual class names for plots
    label_encoder = joblib.load('../models/label_encoder.joblib')
    class_names = label_encoder.classes_

    # 2. Define the models to compare
    # Using random_state ensures reproducibility across different runs
    models = {
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='mlogloss')
    }

    # 3. Train and Evaluate
    results = {}
    best_model_name = ""
    best_accuracy = 0
    best_model = None

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        
        # Predict on test set
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        metrics = evaluate_model(y_test, y_pred, name)
        results[name] = metrics
        
        # Generate Confusion Matrix
        plot_confusion_matrix(y_test, y_pred, class_names, name)
        
        # Print full classification report
        print(f"Classification Report for {name}:\n")
        print(classification_report(y_test, y_pred, target_names=class_names, zero_division=0))
        
        # Select the best model (preferring Random Forest if tied or very close)
        if metrics['Accuracy'] > best_accuracy:
            best_accuracy = metrics['Accuracy']
            best_model_name = name
            best_model = model

    # 4. Compare and Visualize
    plot_model_comparison(results)
    
    print(f"*** Best Model Selected: {best_model_name} with Accuracy: {best_accuracy:.4f} ***")

    # 5. Extract Feature Importance (If Random Forest is selected)
    # We load the preprocessor to get the actual feature names
    preprocessor = joblib.load('../models/preprocessor.joblib')
    # get_feature_names_out() extracts the column names after OneHotEncoding
    feature_names = preprocessor.get_feature_names_out()
    
    # Save the feature names so the Streamlit app knows the exact column order
    joblib.dump(feature_names, '../models/feature_columns.pkl')

    print(f"\nExtracting Feature Importance for {best_model_name}...")
    importances = best_model.feature_importances_
    
    # Create a dataframe of feature importances
    fi_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    # Plot Top 10 Features
    plt.figure(figsize=(10, 6))
    sns.barplot(data=fi_df.head(10), x='Importance', y='Feature', palette='magma')
    plt.title(f'Top 10 Feature Importances - {best_model_name}')
    plt.tight_layout()
    plt.savefig('../plots/rf_feature_importance.png')
    plt.close()
    print("Feature importance plot saved.")

    # 6. Save the Best Model
    # We use joblib because it handles large NumPy arrays (which Scikit-Learn models use internally) better than standard pickle.
    model_path = '../models/best_model.pkl'
    joblib.dump(best_model, model_path)
    
    # Note: We rename the previously saved label encoder to match your exact folder requirements
    os.rename('../models/label_encoder.joblib', '../models/label_encoders.pkl')
    
    print(f"\nModel Saving Complete!")
    print(f"Saved best model to: {model_path}")
    print(f"Saved feature columns to: ../models/feature_columns.pkl")
    print(f"Renamed encoder to: ../models/label_encoders.pkl")

if __name__ == "__main__":
    main()