import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load your labeled dataset (e.g., CSV file with 'content' and 'threat' columns)
data = pd.read_csv('website_content.csv')

# Preprocessing: Clean and tokenize text
# Feature extraction: TF-IDF vectorization
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(data['content'])
y = data['threat']

# Split data into train and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a logistic regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate on validation set
y_pred = model.predict(X_val)
print(classification_report(y_val, y_pred))

# Example inference
def predict(value):
    new_features = vectorizer.transform([value])
    predicted_label = model.predict(new_features)[0]
    print(f"Predicted label: {predicted_label} (0: Safe, 1: Suspicious, 2: Unsafe)")

predict("this is unsafe")
predict("this is safe")
predict("this is suspicious")