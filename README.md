# 📧 CertiMail AI™ — Enterprise Email Security Studio

A machine learning web application built with **Streamlit**, **Scikit-Learn**, and **Pandas** for real-time email spam detection, confidence scoring, keyword impact visualizer, and batch classification.

---

## ✨ Features

- **🔍 Real-Time Email Classifier**: Instant evaluation of email subject & body text into **SPAM** or **HAM (Safe Email)**.
- **📊 Probability & Confidence Metrics**: Displays exact percentage confidence for spam vs ham predictions.
- **🖍️ Keyword Impact Visualizer**: Color-codes and highlights words in the email text that influenced the classifier decision.
- **🚀 Sample Template Selector**: One-click quick loading of realistic email samples (Prize Scams, Phishing, Bank Alerts, Work Sync, Receipts).
- **📂 Batch CSV Classifier**: Upload CSV files or paste multiple email entries to process in bulk with downloadable CSV results.
- **📈 Model Analytics**: Visualize top 20 spam-trigger and ham-trigger word coefficients.

---

## 🚀 Getting Started

### 1. Prerequisites & Virtual Environment

Ensure you have Python 3.10+ installed and activate your virtual environment:

```bash
source .venv/bin/activate
```

### 2. Launch the Streamlit Web Application

To run the web interface, execute:

```bash
streamlit run src/app.py
```

The app will automatically open in your browser at `http://localhost:8501`.

---

## 🛠️ Project Structure

```text
Email_Classifier/
├── src/
│   ├── app.py                      # Main Streamlit Web Application UI
│   └── email_classifier/
│       ├── inferance.py            # Model loading, predictions, and detailed keyword extraction
│       ├── emails.csv              # Model training dataset
│       └── model.pkl               # Saved Logistic Regression model checkpoint
├── pyproject.toml
└── README.md
```
