# src/utils.py
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
import numpy as np
import os

def evaluate_model(y_true, y_pred, model_name):
    """Calculates and prints core classification metrics."""
    acc = accuracy_score(y_true, y_pred)
    # Using 'weighted' because this is a multi-class problem (multiple fertilizers)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    print(f"--- {model_name} Performance ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}\n")
    
    return {'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1': f1}

def plot_confusion_matrix(y_true, y_pred, classes, model_name):
    """Generates and saves a confusion matrix heatmap."""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    
    os.makedirs('../plots', exist_ok=True)
    plt.savefig(f'../plots/cm_{model_name.replace(" ", "_")}.png')
    plt.close()

def plot_model_comparison(metrics_dict):
    """Generates a bar chart comparing model accuracies."""
    models = list(metrics_dict.keys())
    accuracies = [metrics_dict[m]['Accuracy'] for m in models]
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=models, y=accuracies, palette='viridis')
    plt.title('Model Accuracy Comparison')
    plt.ylim(0, 1.1)
    plt.ylabel('Accuracy')
    for i, v in enumerate(accuracies):
        plt.text(i, v + 0.02, f"{v:.4f}", ha='center')
    
    plt.tight_layout()
    plt.savefig('../plots/model_comparison.png')
    plt.close()