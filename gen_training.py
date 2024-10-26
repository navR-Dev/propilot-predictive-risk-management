import csv
import random
import string
from datetime import datetime, timedelta


def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))


def generate_random_task_name():
    # Generates a random task name by creating a random string
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_csv_1(filename):
    fieldnames = [
        'id', 'pid', 'org_id', 'component', 'created_on', 'updated_on',
        'removed_on', 'removed', 'start_date', 'end_date', 'total_stories',
        'completed_stories', 'total_time (days)', 'sprint', 'dependencies', 'task_name'
    ]

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(2000):  # Generate 2000 records
            created_on = datetime.now() - timedelta(days=random.randint(0, 365))
            updated_on = created_on + timedelta(days=random.randint(0, 30))
            removed_on = updated_on + timedelta(days=random.randint(0, 30))
            start_date = created_on
            end_date = start_date + timedelta(days=random.randint(1, 30))

            writer.writerow({
                'id': i,
                'pid': random.randint(1, 10),
                'org_id': random.randint(1, 10),
                'component': random.choice(['frontend', 'backend', 'database', 'analytics']),
                'created_on': created_on.strftime('%Y-%m-%d'),
                'updated_on': updated_on.strftime('%Y-%m-%d'),
                'removed_on': removed_on.strftime('%Y-%m-%d'),
                'removed': random.choice([True, False]),
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'total_stories': random.randint(1, 50),
                'completed_stories': random.randint(1, 50),
                'total_time (days)': (end_date - start_date).days,
                'sprint': random.randint(1, 10),
                'dependencies': random.randint(0, 10),
                'task_name': generate_random_task_name()
            })


generate_csv_1('training.csv')
