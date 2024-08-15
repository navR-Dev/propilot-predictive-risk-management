import random
import csv
from datetime import datetime, timedelta

# Helper function to generate a random date between two dates


def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Helper function to generate a component name


def generate_component_name(existing_components):
    components = ['Authentication', 'User Profiles', 'Payments', 'Notifications',
                  'Reporting', 'Messaging', 'Dashboard', 'Analytics', 'Database']
    available_components = list(set(components) - set(existing_components))
    if not available_components:  # If all components have been used, reset the list
        existing_components.clear()
        available_components = components
    return random.choice(available_components)

# Generate data


def generate_data(num_records):
    data = []
    org_id = 1
    org_components = []

    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)

    for i in range(1, num_records + 1):
        component = generate_component_name(org_components)
        org_components.append(component)

        created_on = random_date(start_date, end_date)
        updated_on = random_date(created_on, end_date)
        removed = random.choice(['Yes', 'No'])
        removed_on = updated_on if removed == 'Yes' else 'N/A'

        start_dt = created_on
        end_dt = random_date(start_dt, end_date)

        total_stories = random.randint(10, 30)
        completed_stories = random.randint(0, total_stories)
        total_time = (end_dt - start_dt).days

        dependency = random.choice(
            org_components[:-1]) if len(org_components) > 1 else 'N/A'

        data.append([
            i,
            org_id,
            component,
            created_on.strftime('%m/%d/%Y'),
            updated_on.strftime('%m/%d/%Y'),
            removed_on if removed_on == 'N/A' else removed_on.strftime(
                '%m/%d/%Y'),
            removed,
            start_dt.strftime('%m/%d/%Y'),
            end_dt.strftime('%m/%d/%Y'),
            total_stories,
            completed_stories,
            total_time,
            dependency
        ])
    return data

# Write data to CSV


def write_to_csv(data, filename):
    header = ['id', 'org_id', 'component', 'created_on', 'updated_on', 'removed_on', 'removed',
              'start_date', 'end_date', 'total_stories', 'completed_stories', 'total_time (days)', 'dependency']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)


# Generate and write data
data = generate_data(50)  # Generate 50 records
write_to_csv(data, 'output.csv')
