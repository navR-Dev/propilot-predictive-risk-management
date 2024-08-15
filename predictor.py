import pandas as pd
from datetime import datetime

# Function to get user input for the current date


def get_current_date():
    date_str = input("Enter the current date (MM/DD/YYYY): ")
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
        return get_current_date()


# Load the data from output.csv
df = pd.read_csv('output.csv')

# Get the current date from the user
current_date = get_current_date()

# Helper function to predict if a component will finish on time


def predict_finish(df, current_date):
    for index, row in df.iterrows():
        # Calculate days remaining
        end_date = datetime.strptime(row['end_date'], '%m/%d/%Y')
        days_remaining = (end_date - current_date).days

        # Calculate progress
        stories_remaining = row['total_stories'] - row['completed_stories']

        if days_remaining > 0:
            daily_rate_needed = stories_remaining / days_remaining
        else:
            daily_rate_needed = float('inf')

        daily_rate_current = row['completed_stories'] / \
            row['total_time (days)']

        # Predict if the component will finish on time
        if daily_rate_current >= daily_rate_needed:
            prediction = 'On Time'
            advice = 'Keep up the current pace.'
        elif days_remaining <= 0:
            prediction = 'Behind Schedule'
            advice = 'Deadline has passed or is today. Immediate action required.'
        else:
            prediction = 'Behind Schedule'
            advice = f'Increase the daily completion rate to at least {
                daily_rate_needed:.2f} stories/day.'

        # Display the results
        print(f"Component: {row['component']}")
        print(f"Prediction: {prediction}")
        print(f"Advice: {advice}\n")


# Predict and display the results
predict_finish(df, current_date)
