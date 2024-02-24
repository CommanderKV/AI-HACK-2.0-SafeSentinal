import sys
import requests
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import numpy as np

def load_ai():
    # Load the AI model here
    model = load("ai.joblib")
    return model

def analyze_content(link):
    # Fetch the content from the link
    try:
        response = requests.get(link, timeout=3)
    except Exception as e:
        return "[ERROR] Failed to fetch the content from the link."
    content = response.text

    if content is None or content == "":
        return "[ERROR] Failed to fetch the content from the link."

    # Load the AI model
    model = load_ai()

    # Run the content through the AI model
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform([content])

    # Check if the number of features is less than 1000
    if X.shape[1] < 1000:
        # Add additional features with zero values
        zero_features = np.zeros((X.shape[0], 1000 - X.shape[1]))
        X = np.hstack((X.toarray(), zero_features))

    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)

    result = model.predict(X)[0]

    return result

if __name__ == "__main__":
    link = sys.argv[1]
    result = analyze_content(link)
    print(f"Received: {link}")
    print(f"Analysis Result: {"SAFE" if result == 0 else "UNSAFE" if result == 2 else "SUSPICIOUS" if result == 1 else result}")