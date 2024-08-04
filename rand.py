import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Generate fresh sample dataset with specified columns
np.random.seed(42)
data_fresh = {
    'budget': np.random.randint(50000, 100000, 20),
    'team_size': np.random.randint(5, 10, 20),
    'project_duration_days': np.random.randint(30, 60, 20),
    'complexity': np.random.randint(1, 6, 20),  # 1 (low) to 5 (high)
    'on_time': np.random.randint(0, 2, 20)  # 0 (not on time), 1 (on time)
}

df_fresh = pd.DataFrame(data_fresh)

# Features and target variable
X = df_fresh[['budget', 'team_size', 'project_duration_days', 'complexity']]
y = df_fresh['on_time']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# Create and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:")
print(report)

# Display the confusion matrix using a heatmap
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=[
            'Not On Time', 'On Time'], yticklabels=['Not On Time', 'On Time'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Predict on the entire dataset
df_fresh['predicted_on_time'] = model.predict(X)

# Display results
print("\nProject Completion Predictions:")
print(df_fresh)
