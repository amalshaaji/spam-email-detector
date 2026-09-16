# CertiMail — Email Spam Classifier

A machine learning application that classifies emails as **Spam** or **Ham** using natural language processing and supervised learning.

Built with **Python, Scikit-Learn, Pandas, and Streamlit**, the application provides single-email predictions, probability scores, keyword analysis, and batch classification.

## Features

### Email Classification

Classifies email content as:

* **Spam**
* **Ham**

Users can enter an email subject and body directly through the web interface.

### Prediction Probability

Displays the model's predicted probability for both Spam and Ham classes, providing additional context for each classification.

### Keyword Analysis

Identifies and highlights words that have a stronger contribution to the model's classification decision.

### Sample Emails

Includes predefined examples for testing different types of messages, including:

* Prize and promotional messages
* Phishing emails
* Bank alerts
* Work-related emails
* Purchase receipts

### Batch Classification

Supports CSV uploads for processing multiple emails at once.

The processed results can be exported as a CSV file for further analysis.

### Model Analysis

Provides insights into the features learned by the model, including the words with the strongest Spam and Ham coefficients.

## Tech Stack

| Technology          | Purpose                                      |
| ------------------- | -------------------------------------------- |
| Python              | Application and machine learning development |
| Scikit-Learn        | Model training and text classification       |
| Pandas              | Dataset and CSV processing                   |
| Streamlit           | Web application interface                    |
| TF-IDF              | Text feature extraction                      |
| Logistic Regression | Email classification                         |

## Machine Learning Pipeline

```text
Email
  ↓
Text Preprocessing
  ↓
TF-IDF Vectorization
  ↓
Logistic Regression
  ↓
Spam / Ham Classification
  ↓
Probability & Keyword Analysis
```

The model converts email text into numerical features using **TF-IDF (Term Frequency–Inverse Document Frequency)**. These features are then used by a Logistic Regression classifier to distinguish between Spam and Ham emails.

## Project Structure

```text
Email_Classifier/
│
├── src/
│   ├── app.py
│   │
│   └── email_classifier/
│       ├── inferance.py
│       ├── emails.csv
│       └── model.pkl
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

### File Description

| File               | Description                              |
| ------------------ | ---------------------------------------- |
| `app.py`           | Streamlit application and user interface |
| `inferance.py`     | Model loading and prediction logic       |
| `emails.csv`       | Dataset used for model training          |
| `model.pkl`        | Trained Logistic Regression model        |
| `pyproject.toml`   | Project configuration                    |
| `requirements.txt` | Project dependencies                     |

## Getting Started

### Prerequisites

* Python 3.10+
* pip
* Virtual environment

### Clone the Repository

```bash
git clone https://github.com/amalshaaji/spam-email-detector.git
cd spam-email-detector
```

### Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run src/app.py
```

The application will start locally at:

```text
http://localhost:8501
```

## Example

### Spam Email

```text
Congratulations! You have won a $1,000 prize.
Click the link below to claim your reward.
```

**Prediction:** `SPAM`

### Ham Email

```text
Hi John,

The meeting has been moved to 3 PM tomorrow.
Please let me know if you can attend.

Thanks.
```

**Prediction:** `HAM`

## Classification Workflow

For a single email:

1. Enter the email subject and body.
2. Submit the email for classification.
3. The text is transformed using TF-IDF.
4. The trained Logistic Regression model generates a prediction.
5. The application displays the classification and probability scores.
6. Relevant model features can be inspected through keyword analysis.

For batch processing, users can upload a CSV containing multiple email records and generate predictions for the entire dataset.

## Model

The project uses **Logistic Regression**, a supervised learning algorithm commonly used for binary classification.

The model is trained on labelled email data:

```text
Email Text → TF-IDF Features → Logistic Regression → Spam / Ham
```

The trained model is stored as `model.pkl` and loaded by the application during inference.

## Limitations

The model's performance depends on the quality and variety of the training dataset.

It may produce incorrect classifications for:

* Unusual email formats
* Previously unseen wording
* Highly obfuscated messages
* Emails containing mixed Spam and legitimate content
* Messages significantly different from the training data

Therefore, predictions should be treated as model outputs rather than definitive email-security decisions.

## Future Improvements

* Improve the training dataset
* Add model evaluation metrics
* Add confusion matrix and classification reports
* Experiment with alternative classification algorithms
* Improve text preprocessing
* Add model retraining support
* Deploy the application as a web service
* Add automated model evaluation

## License

This project is available for educational and portfolio use.

