import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/matches_2014_present.csv")
df = df.dropna()

features = [
    "elo_difference",
    "form_difference",
    "goal_difference"
]

X = df[features]
y = df["result"]

# Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Logistic Regression model
model = LogisticRegression(max_iter=1000, class_weight="balanced")

model.fit(X_train, y_train)

with open("models/logistic_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model and scaler saved!")

# Make predictions 
predictions = model.predict(X_test)
print(predictions[:10])

# Evaluate accuracy
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy:.2f}")

print(confusion_matrix(y_test, predictions))

# Full evaluation 
print(classification_report(y_test, predictions))

for feature, coef in zip(features, model.coef_[0]):
    print(f"{feature}: {coef:.4f}")

importance = pd.DataFrame({
    "feature": features,
    "importance": abs(model.coef_).mean(axis=0)
})