# 🌱 Vibe-FrameTric

### AI-Powered Sustainable Fertilizer Intelligence System for Smart Agriculture

Vibe-FrameTric is an AI-assisted agronomy intelligence platform that combines **Machine Learning**, **rule-based sustainability analysis**, and **interactive visualization** to recommend fertilizers while detecting potential nutrient overuse patterns and soil sustainability risks.

The system is designed as a practical prototype for addressing fertilizer misuse and unsustainable nutrient management in Indian agriculture.

---

# 🚀 Project Overview

Modern agriculture often suffers from:

* excessive fertilizer dependency
* nutrient imbalance
* declining soil health
* inefficient fertilizer application
* salinity buildup due to repeated chemical usage

Vibe-FrameTric aims to provide:

* intelligent fertilizer recommendation
* nutrient stress analysis
* sustainability scoring
* explainable agronomy insights

using a hybrid architecture combining:

* **XGBoost Machine Learning**
* **Heuristic Sustainability Intelligence**
* **Interactive Streamlit Dashboard**

---

# ✨ Key Features

## 🤖 AI Fertilizer Recommendation

Predicts the most suitable fertilizer based on:

* soil conditions
* environmental parameters
* crop information
* nutrient levels

---

## 🌾 NPK Overuse Detection

Detects potential:

* Nitrogen excess
* Phosphorus accumulation
* Potassium over-application

using explainable agronomy-inspired logic.

---

## ⚠️ Sustainability Risk Analysis

Analyzes:

* nutrient imbalance
* salinity risk
* repeated fertilizer dependency
* poor fertilizer efficiency
* low soil organic carbon

---

## 📊 Sustainability Scoring Engine

Generates:

* sustainability score (0–100)
* risk level
* penalty breakdown
* warning indicators

---

## 💡 Explainable Recommendations

Provides:

* fertilizer optimization suggestions
* crop rotation tips
* soil health recommendations
* balanced fertilization advice

---

## 🖥️ Interactive Dashboard

Built using **Streamlit** with:

* sliders
* dropdowns
* metric cards
* warnings panel
* sustainability analytics

---

# 🧠 System Architecture

```text id="vdzrb0"
User Input
   │
   ▼
Data Preprocessing
   │
   ▼
XGBoost Fertilizer Recommendation Model
   │
   ├──────────────┐
   ▼              ▼
Overuse Engine   Sustainability Engine
   │              │
   └──────┬───────┘
          ▼
 AI-Assisted Agronomy Insights
          ▼
 Streamlit Dashboard Output
```

---

# 🛠️ Tech Stack

## Machine Learning

* Python
* Scikit-learn
* XGBoost
* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn
* Plotly

## Frontend

* Streamlit

## Model Serialization

* Joblib
* Pickle

---

# 📂 Project Structure

```text id="a9nphj"
Vibe-Farmetric/
│
├── app/
│   ├── streamlit_app.py
│   ├── predictor.py
│   ├── overuse_engine.py
│   ├── sustainability.py
│   ├── config.py
│   └── utils.py
│
├── models/
│   ├── best_model.pkl
│   ├── encoders.pkl
│   └── feature_columns.pkl
│
├── notebooks/
│   ├── 01_data_preprocessing.ipynb
│   └── 02_exploratory_data_analysis.ipynb
|
├── src/
│   ├── train_model.py
│   └── utils.py
│
├── data/
│   └── fertilizer_dataset.csv
│
├── plots/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 📊 Dataset Information

The dataset contains:

* soil properties
* environmental conditions
* crop information
* nutrient levels
* fertilizer usage patterns

### Main Features

* Soil_Type
* Soil_pH
* Nitrogen_Level
* Phosphorus_Level
* Potassium_Level
* Temperature
* Humidity
* Rainfall
* Crop_Type
* Season
* Organic_Carbon
* Electrical_Conductivity
* Yield_Last_Season

### Target

* Recommended_Fertilizer

---

# 🔍 Exploratory Data Analysis

The project includes:

* class distribution analysis
* feature importance analysis
* nutrient correlation analysis
* sustainability trend exploration
* outlier detection
* soil parameter visualization

---

# 🤖 Machine Learning Pipeline

## Models Trained

* Decision Tree
* Random Forest
* XGBoost

## Final Selected Model

### ✅ XGBoost Classifier

Chosen because it achieved:

* highest overall accuracy
* better class balancing
* stronger weighted F1-score

---

# 📈 Model Performance

| Metric    | Score  |
| --------- | ------ |
| Accuracy  | ~87.6% |
| Precision | ~87.3% |
| Recall    | ~87.6% |
| F1-Score  | ~87.4% |

---

# 🌱 Sustainability Intelligence Engine

The sustainability engine uses:

* heuristic nutrient analysis
* weighted risk scoring
* agronomy-inspired rules

to detect:

* nutrient stress
* salinity risks
* fertilizer dependency
* poor soil efficiency patterns

---

# ⚠️ Important Scientific Note

This project is:

* an AI-assisted prototype
* a heuristic sustainability analysis system

It is **NOT**:

* a certified agronomic diagnostic system
* a replacement for laboratory soil testing
* scientifically conclusive agricultural advisory software

All outputs should be interpreted as:

> “Potential sustainability indicators and fertilizer optimization insights.”

---

# 🖥️ Streamlit Dashboard Features

## User Inputs

* Soil Type
* NPK Levels
* pH
* Temperature
* Rainfall
* Crop Type
* Season
* Previous Fertilizer
* Organic Carbon
* EC Levels

---

## Dashboard Outputs

- ✅ Recommended Fertilizer

- ⚠️ Risk Level

- 🌱 Sustainability Score

- 📋 Warning Indicators

- 💡 Agronomy Recommendations

---

# ⚙️ Installation

## 1. Clone Repository

```bash id="18x7iq"
git clone https://github.com/your-username/Vibe-FrameTric.git
cd Vibe-FrameTric
```

---

## 2. Create Virtual Environment

### Windows

```bash id="u8afgf"
python -m venv venv
venv\Scripts\activate
```

### Linux/Mac

```bash id="r5yy7f"
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash id="g8x56j"
pip install -r requirements.txt
```

---

# ▶️ Run the Application

```bash id="v40p3u"
streamlit run app/streamlit_app.py
```

---

# 🧪 Example Output

```json id="5f8j9m"
{
  "recommended_fertilizer": "DAP",
  "sustainability_score": 72,
  "risk_level": "Moderate",
  "warnings": [
    "Potential nutrient imbalance detected",
    "Elevated salinity risk observed"
  ],
  "recommendations": [
    "Reduce excessive nitrogen application",
    "Adopt balanced fertilization"
  ]
}
```

---

# 📌 Future Improvements

* Real-world agricultural datasets
* IoT soil sensor integration
* Satellite/weather API integration
* Explainable AI (SHAP/LIME)
* Mobile application
* Multilingual farmer support
* Geo-specific agronomy tuning
* Real-time soil analytics

---

# 🎯 Use Cases

* Smart farming systems
* Precision agriculture research
* Agritech demonstrations
* Sustainability analytics
* Educational AI projects
* Fertilizer optimization studies

---

# 🌍 Vision

Vibe-FrameTric aims to demonstrate how AI can support more sustainable agricultural practices by combining:

* machine learning
* explainable intelligence
* sustainability awareness
* interactive analytics

into a unified agritech decision-support prototype.

---


# 👩‍💻 Author

### Ahana Banerjee

Electronics & Communication Engineering 
JNTUH Hyderabad

