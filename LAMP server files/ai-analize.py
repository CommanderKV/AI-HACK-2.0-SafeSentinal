import sys
import csv
import pandas as pd
import requests
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MaxAbsScaler, MinMaxScaler
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

    scaler = MaxAbsScaler()
    X = scaler.fit_transform(X)

    result = model.predict(X)[0]

    return result

def classify_website(url, type_category):
    safeCategories = ["benign", "safe"]
    suspiciousCategories = ['defacement', "unsure"]
    unsafeCategories = ["malware", "phishing"]
    if type_category in safeCategories:
        return 0
    elif type_category in suspiciousCategories:
        return 1
    elif type_category in unsafeCategories:
        return 2
    else:
        print("UNKNOWN THREAT TYPE: ", type_category, "for URL: ", url, "Skipping...")
        return -1

if __name__ == "__main__":
    """
    with open("../malicious_phish.csv", "r") as file:
        data = csv.reader(file)
        next(data)
        results = []

        try:
            for row in data:
                try:
                    link = row[0]
                    value = classify_website(row[0], row[1])
                    result = analyze_content(link)
                    results.append((value, result))
                    print(value)
                except:
                    print("Failed to analyze", row)
        except:
            print("Failed to loop csv file.")
        
        totalSum = sum([1 if item[0] == item[1] else 0 for item in results])
        print("Sum:", totalSum)
        print("Length:", len(results))
        print("Average:", totalSum / len(results))


    """
    link = sys.argv[1]
    result = analyze_content(link)
    print(f"Received: {link}")
    print(f"Analysis Result: {result} / {"SAFE" if result == 0 else "UNSAFE" if result == 2 else "SUSPICIOUS" if result == 1 else result}")
    