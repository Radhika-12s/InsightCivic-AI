# ◆ InsightCivic AI

### Civic Intelligence & Emergency Risk Analysis Platform

InsightCivic AI is a **model-assisted civic intelligence platform** that analyzes historical civic and environmental observations and uses a trained **Random Forest classification model** to classify emergency risk levels.

The platform provides an interactive workspace for exploring data, analyzing individual observations, reviewing model explanations, saving analysis history, and generating PDF reports.

> **Responsible Use:** InsightCivic AI is a decision-support and analytical system. Model outputs are not guarantees of real-world emergencies, and feature importance should not be interpreted as causal evidence.

---

## 📌 Project Overview

Urban environments generate large amounts of historical information related to incidents, crashes, weather conditions, and time-based patterns.

InsightCivic AI provides a structured interface for analyzing these observations and reviewing a machine-learning-based emergency risk classification.

The application combines:

* Historical dataset exploration
* Observation-based risk analysis
* Random Forest classification
* Model feature importance
* Analysis history
* PDF report generation
* User authentication
* Role-based administrative access

---

## 🎯 Objectives

The main objectives of InsightCivic AI are to:

1. Analyze historical civic and environmental observations.
2. Provide model-assisted emergency risk classification.
3. Allow users to inspect the observations used for analysis.
4. Present model feature importance for interpretability.
5. Store completed analyses for later review.
6. Generate structured PDF reports.
7. Provide authenticated user access.
8. Support role-based access for administrative functionality.

---

## ✨ Key Features

### 🔐 Authentication

Users can create an account and securely sign in to the platform.

The application supports:

* User registration
* User login
* Password-based authentication
* Logout
* User roles

---

### ◉ Risk Analysis

Users can select a specific:

* Date
* Hour

The system retrieves the corresponding observation and sends selected features to the trained Random Forest model.

The analysis displays:

* Risk classification
* Model probability score
* Crime count
* Crash count
* Rainfall
* Temperature
* Peak-hour indicator

---

### 📊 Visual Analysis

The Risk Analysis section provides visual evidence including:

* Daily risk-score distribution
* Crime vs. crash relationship

The selected observation is highlighted in the visualizations.

---

### 🧠 Model Explanation

The application displays feature importance from the trained Random Forest model.

The system identifies the feature with the highest model importance for the selected model configuration.

> Feature importance describes the contribution of an input within the trained model. It does not establish that the feature causes emergency risk.

---

### ▦ Dataset Explorer

Users can inspect the application's working dataset.

The explorer provides:

* Dataset dimensions
* Missing-value information
* Dataset preview
* CSV upload and preview

Uploaded CSV files are previewed without replacing the application's primary dataset.

---

### ◷ Analysis History

Authenticated users can save their completed analyses.

Saved records include information such as:

* Analysis date
* Hour
* Crime count
* Crash count
* Rainfall
* Temperature
* Peak-hour indicator
* Risk classification
* Model confidence
* Top model factor
* Creation timestamp

Users can revisit their saved analyses through **My History**.

---

### 📄 PDF Report Generation

InsightCivic AI can generate a structured PDF report containing:

* Analysis date and hour
* Risk classification
* Model probability score
* Selected observation
* Model explanation
* Risk-score visualization
* Crime vs. crash visualization
* Responsible-use statement

---

### ⚙️ Role-Based Administration

The application supports two user roles:

```text
User
 ├── Overview
 ├── Risk Analysis
 ├── Dataset Explorer
 └── My History

Admin
 ├── Overview
 ├── Risk Analysis
 ├── Dataset Explorer
 ├── My History
 └── Admin Panel
```

Administrative functionality is restricted to accounts with the `admin` role.

The Admin Panel provides an overview of registered users and their roles.

---

## 🔄 Application Workflow

```text
Historical Dataset
        │
        ▼
   Data Processing
        │
        ▼
 Observation Selection
        │
        ▼
 Feature Extraction
        │
        ▼
 Random Forest Model
        │
        ▼
 Risk Classification
        │
        ├──────────────► Visual Analysis
        │
        ├──────────────► Model Explanation
        │
        ├──────────────► Save Analysis
        │
        └──────────────► PDF Report
```

---

## 🧠 Machine Learning

The application uses a trained **Random Forest classification model** for emergency risk classification.

### Model Input Features

The application currently uses the following features for the risk classification workflow:

| Feature        | Description                                 |
| -------------- | ------------------------------------------- |
| `crime_count`  | Crime count associated with the observation |
| `crash_count`  | Crash count associated with the observation |
| `PRCP`         | Precipitation / rainfall value              |
| `TAVG`         | Average temperature                         |
| `is_peak_hour` | Indicator for peak-hour observation         |

The trained model is loaded from:

```text
models/emergency_risk_model.pkl
```

---

## 📁 Project Structure

```text
InsightCivic-AI/
│
├── app/
│   └── ...
│
├── data_processed/
│   └── final_emergency_hourly_dataset.csv
│
├── data_raw/
│   └── ...
│
├── database/
│   └── ...
│
├── models/
│   └── emergency_risk_model.pkl
│
├── src/
│   └── ...
│
├── create_admin.py
├── requirements.txt
└── README.md
```

> The exact contents of some folders may change as the project evolves.

---

## 🛠️ Technology Stack

### Programming Language

* Python

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* Random Forest

### Visualization

* Matplotlib

### Web Application

* Streamlit

### Database

* SQLite

### Authentication

* Python-based authentication system
* Password hashing

### Reporting

* ReportLab

### Model Serialization

* Joblib

### Deployment

* Streamlit Community Cloud

---

## 💻 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Radhika-12s/InsightCivic-AI.git
```

### 2. Open the project

```bash
cd InsightCivic-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

Run the Streamlit application using the project's configured application entry point.

For example:

```bash
streamlit run app/app.py
```

If your local project uses a different entry file, use that configured entry point instead.

---

## 🔑 User Access

After launching the application:

1. Create an account using **Create account**.
2. Sign in using the registered credentials.
3. Open **Risk Analysis**.
4. Select an observation date and hour.
5. Review the model classification.
6. Inspect the visual analysis and model explanation.
7. Save the analysis if required.
8. Review saved results under **My History**.
9. Generate a PDF report when required.

---

## 🗄️ Database

InsightCivic AI uses SQLite for application-level storage.

The database stores:

### Users

* User ID
* Username
* Email
* Password hash
* Role
* Account creation time
* Last login

### Analysis History

* User ID
* Analysis date
* Analysis hour
* Observation values
* Risk level
* Confidence score
* Top model factor
* Creation timestamp

---

## 🧪 Application Modules

| Module           | Purpose                                |
| ---------------- | -------------------------------------- |
| Authentication   | Registration and login                 |
| Overview         | Workspace and dataset summary          |
| Risk Analysis    | Model-assisted risk classification     |
| Dataset Explorer | Dataset inspection and CSV preview     |
| My History       | Saved user analyses                    |
| Admin Panel      | Administrative user overview           |
| PDF Reporting    | Generate downloadable analysis reports |

---

## 📈 Responsible Use

InsightCivic AI is designed as an **analytical decision-support platform**.

The system should not be used as a standalone mechanism for making real-world emergency decisions.

Important limitations include:

* Historical patterns do not guarantee future events.
* Model classifications are not certainties.
* A model probability score should not automatically be interpreted as the probability of a real-world emergency.
* Feature importance does not establish causation.
* Results should be reviewed alongside appropriate real-world context and domain expertise.

---

## 🔮 Future Scope

Potential future improvements include:

* Integration with real-time civic data sources
* More comprehensive geographic analysis
* Interactive mapping
* Additional machine-learning models
* Model performance monitoring
* Improved administrative controls
* More detailed analytics dashboards
* Automated scheduled reporting
* Cloud-based persistent database infrastructure
* Enhanced model evaluation and monitoring

---

## 📚 Project Purpose

InsightCivic AI was developed as an academic project to demonstrate the integration of:

* Python programming
* Data processing
* Machine learning
* Data visualization
* Database management
* Authentication
* Role-based access
* Web application development
* Report generation

The project demonstrates how these technologies can be combined into a single interactive analytical application.

---

## 👩‍💻 Author

**Radhika Ashok Bhadoriya**

BCA Student
Prestige Institute of Management & Research, Gwalior

### Project

**InsightCivic AI — Civic Intelligence & Emergency Risk Analysis Platform**

---

## 🔗 Links

* 🌐 **Live Application:** https://insightcivic-ai.streamlit.app/
* 💻 **GitHub Repository:** https://github.com/Radhika-12s/InsightCivic-AI

---

## ⭐ Project Status

**Status: Completed Academic Project**

The deployed application currently provides authentication, civic-risk analysis, dataset exploration, analysis history, model explanation, PDF reporting, and role-based administrative functionality.
