from collections import Counter
from pathlib import Path
import re

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression


BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "emails.csv"
MODEL_PATH = BASE_DIR / "model.pkl"


def train_model():
    df = pd.read_csv(DATASET_PATH).dropna()

    feature_columns = df.columns.difference(["Email No.", "Prediction"])
    X = df[feature_columns]
    y = df["Prediction"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    return model, feature_columns


def load_model():
    df = pd.read_csv(DATASET_PATH, nrows=1)
    feature_columns = df.columns.difference(["Email No.", "Prediction"])

    if MODEL_PATH.exists():
        model = joblib.load(MODEL_PATH)
    else:
        model, feature_columns = train_model()

    return model, feature_columns


def predict_email(email_text):
    details = predict_email_details(email_text)
    return details["prediction"]


def predict_email_details(email_text):
    model, feature_columns = load_model()

    words = re.findall(r"\b\w+\b", email_text.lower())
    word_counts = Counter(words)

    email_features = pd.DataFrame(
        [[word_counts.get(column.lower(), 0) for column in feature_columns]],
        columns=feature_columns,
    )

    prediction = int(model.predict(email_features)[0])

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(email_features)[0]
        prob_ham = float(probabilities[0])
        prob_spam = float(probabilities[1])
    else:
        prob_spam = 1.0 if prediction == 1 else 0.0
        prob_ham = 1.0 - prob_spam

    word_contributions = []
    if hasattr(model, "coef_"):
        coefs = model.coef_[0]
        feature_list = list(feature_columns)
        for w in set(words):
            w_lower = w.lower()
            matching_cols = [c for c in feature_list if c.lower() == w_lower]
            for col in matching_cols:
                idx = feature_list.index(col)
                count = word_counts[w_lower]
                weight = coefs[idx]
                word_contributions.append(
                    {
                        "word": col,
                        "count": count,
                        "coef": float(weight),
                        "impact": float(count * weight),
                    }
                )

    word_contributions.sort(key=lambda x: abs(x["impact"]), reverse=True)

    return {
        "prediction": prediction,
        "is_spam": prediction == 1,
        "prob_spam": prob_spam,
        "prob_ham": prob_ham,
        "total_words": len(words),
        "word_contributions": word_contributions,
    }


def get_top_spam_words(n=20):
    model, feature_columns = load_model()
    if hasattr(model, "coef_"):
        coefs = model.coef_[0]
        df_coef = pd.DataFrame(
            {"word": list(feature_columns), "coefficient": coefs}
        )
        top_spam = df_coef.sort_values(
            by="coefficient", ascending=False
        ).head(n)
        top_ham = df_coef.sort_values(by="coefficient", ascending=True).head(n)
        return top_spam, top_ham
    return None, None


if __name__ == "__main__":
    email = input("Enter your email: ")
    prediction = predict_email(email)

    if str(prediction) == "1":
        print("\nPrediction: SPAM")
    else:
        print("\nPrediction: NOT SPAM")