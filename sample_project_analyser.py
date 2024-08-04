import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load data from CSV
df = pd.read_csv('propilot_test.csv')

# Adding random columns
np.random.seed(42)
df['budget'] = np.random.randint(50000, 100000, df.shape[0])
df['team_size'] = np.random.randint(5, 10, df.shape[0])

# Calculate project_duration_days
df['start_date'] = pd.to_datetime(df['start_date'], format='%d/%m/%Y')
df['end_date'] = pd.to_datetime(df['end_date'], format='%d/%m/%Y')
df['project_duration_days'] = (df['end_date'] - df['start_date']).dt.days

# Adding a complexity column with random values
df['complexity'] = np.random.randint(1, 6, df.shape[0])

# Derive 'on_time' based on the 'status' column (arbitrarily setting 'ongoing' as 1 and 'cancelled' as 0)
df['on_time'] = df['Status'].apply(lambda x: 1 if x == 'ongoing' else 0)

# Data exploration
print(df.head())
print(df.describe())
sns.pairplot(df[['budget', 'team_size', 'project_duration_days', 'complexity', 'on_time']], hue='on_time')
plt.show()

# Features and target variable
X = df[['budget', 'team_size', 'project_duration_days', 'complexity']]
y = df['on_time']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

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
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=['Not On Time', 'On Time'], yticklabels=['Not On Time', 'On Time'])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Predict on the entire dataset
df['predicted_on_time'] = model.predict(X)

# Display results
print("\nProject Completion Predictions:")
print(df[['budget', 'team_size', 'project_duration_days', 'complexity', 'on_time', 'predicted_on_time']])
