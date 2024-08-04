import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# Load the data
data = pd.read_csv('generated_data.csv')

# Handle missing values by dropping rows with missing values in the selected columns
data = data.dropna(subset=['org_id\t', 'createdById', 'removed'])

# Create a target variable 'completed' which is True if 'removed' is False
data['completed'] = ~data['removed']

# Select features and the target variable
features = ['org_id\t', 'createdById', 'removed']
target = 'completed'
X = data[features]
y = data[target].astype(int)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Train the Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Report:\n{report}')

# Predicting the likelihood of a new project being completed
input_org_id = 1234  # Replace with actual org_id
input_createdById = 5  # Replace with actual createdById
input_removed = False  # Replace with actual removed status

new_project = pd.DataFrame({
    'org_id\t': [input_org_id],
    'createdById': [input_createdById],
    'removed': [input_removed]
})

# Predict probability of completion
completion_prob = model.predict_proba(
    new_project)[:, 1]  # Probability of completion
print(f'Likelihood of completion: {completion_prob[0]}')
