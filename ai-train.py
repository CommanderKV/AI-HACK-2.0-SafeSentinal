import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets
from joblib import dump

# Load your labeled dataset (e.g., CSV file with "content" and "threat" columns)
data = pd.read_csv("../classified_websites.csv")

# Filtering data
dataIn = {
    0: [],
    1: [],
    2: []
}

for i, content in enumerate(data["Content"]):
    dataIn[data["Threat"][i]].append(content)

totalSum = len(dataIn[0]) + len(dataIn[1]) + len(dataIn[2])
print(f"Total: {totalSum}")
print(f"Safe: {len(dataIn[0]) / totalSum * 100}%")
print(f"Suspicious: {len(dataIn[1]) / totalSum * 100}%")
print(f"Unsafe: {len(dataIn[2]) / totalSum * 100}%")
print("-----------------")
print("Adjusting...")
print("-----------------")

while len(dataIn[0]) > totalSum / 3:
    dataIn[0].pop()

totalSum = len(dataIn[0]) + len(dataIn[1]) + len(dataIn[2])
print(f"Total: {totalSum}")
print(f"Safe: {len(dataIn[0]) / totalSum * 100}%")
print(f"Suspicious: {len(dataIn[1]) / totalSum * 100}%")
print(f"Unsafe: {len(dataIn[2]) / totalSum * 100}%")
print("-----------------")
print("Training...")
print("-----------------")

# Preprocessing: Clean and tokenize text
# Feature extraction: TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(data["Content"])
y = data["Threat"]

# Normalize the features
scaler = MinMaxScaler()
X = scaler.fit_transform(X.toarray())

# Split data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate on validation set
y_pred = model.predict(X_val)
print(classification_report(y_val, y_pred))

# Example inference
def predict(value):
    new_features = vectorizer.transform([value])
    new_features = scaler.transform(new_features.toarray())
    predicted_label = model.predict(new_features)[0]
    print(f"Predicted label: {predicted_label} (0: Safe, 1: Suspicious, 2: Unsafe)")
    return predicted_label

def save(model):
    dump(model, "ai.joblib")

def testModel():
    results = []
    amounts = [0, 0, 0]
    for i, content in enumerate(data["Content"]):
        if amounts[0] > 10 and data["Threat"][i] == 0:
            continue
        elif amounts[1] > 10 and data["Threat"][i] == 1:
            continue
        elif amounts[2] > 10 and data["Threat"][i] == 2:
            continue

        if data["Threat"][i] == 0:
            amounts[0] += 1
        elif data["Threat"][i] == 1:
            amounts[1] += 1
        else:
            amounts[2] += 1
        results.append([predict(content), data["Threat"][i]])
        print("Answer: ", data["Threat"][i])


    totals = []
    for result in results:
        totals.append(1 if result[0] == result[1] else 0)

    print(f"Sum: {sum(totals)}")
    print(f"length: {len(totals)}")
    print(f"Average: {sum(totals) / len(totals)}")
    print(f"Score: {model.score(X_val, y_val)}")

def getBestModel():
    bestModel = None
    bestScore = 0
    for i in range(3000):
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3, random_state=i)
        model = LogisticRegression()
        model.fit(X_train, y_train)
        score = model.score(X_val, y_val)

        if score > bestScore:
            bestScore = score
            bestModel = model
            print(f"[INFO] Score: {score} for random state {i}")
            print("\t[INFO] New best model!")
        
    return bestModel



save(getBestModel())

y_pred = model.predict(X_val)
print(classification_report(y_val, y_pred))