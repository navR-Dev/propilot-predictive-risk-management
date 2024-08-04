import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime

# Load the dataset
data = pd.read_csv('propilot_test.csv')

# Preprocess the data
# Convert dates to datetime objects
data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])

# Calculate the duration of each project in days
data['duration'] = (data['end_date'] - data['start_date']).dt.days

# Filter out any rows with missing values in 'total_stories' or 'completed_stories'
data = data.dropna(subset=['total_stories', 'completed_stories'])

# Define features and target
X = data[['duration', 'total_stories']]
y = data['completed_stories']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Create a linear regression model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Predict whether a project will finish on time


def predict_completion(org_id, start_date, end_date, total_stories):
    # Calculate the duration of the new project
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    duration = (end_date - start_date).days

    # Create a DataFrame for the new project
    new_data = pd.DataFrame(
        {'duration': [duration], 'total_stories': [total_stories]})

    # Predict the number of completed stories
    predicted_completed_stories = model.predict(new_data)[0]

    # Compare predicted completed stories with total stories to determine if the project will finish on time
    if predicted_completed_stories >= total_stories:
        return "The project is predicted to finish on time."
    else:
        return "The project is predicted to finish late."


# Example usage
org_id = 1
start_date = '2024-07-15'
end_date = '2024-08-15'
total_stories = 50

result = predict_completion(org_id, start_date, end_date, total_stories)
print(result)
