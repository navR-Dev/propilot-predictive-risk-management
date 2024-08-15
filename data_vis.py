import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx

# Load the data
data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8],
    'org_id': [101, 102, 101, 103, 104, 102, 103, 104],
    'component': ['Authentication', 'User Profiles', 'Payments', 'Notifications', 'Reporting', 'Messaging', 'Dashboard', 'Analytics'],
    'total_stories': [15, 20, 30, 10, 18, 12, 25, 22],
    'completed_stories': [15, 10, 25, 10, 15, 10, 20, 18],
    'total_time (days)': [44, 56, 65, 47, 60, 49, 51, 61],
    'dependency': ['Database', 'Authentication', 'Authentication', 'Messaging', 'Analytics', 'User Profiles', 'Notifications', 'Reporting']
})

# Bar Chart of Total Stories vs. Completed Stories per Component
plt.figure(figsize=(12, 6))
sns.barplot(x='component', y='total_stories', data=data,
            color='skyblue', label='Total Stories')
sns.barplot(x='component', y='completed_stories', data=data,
            color='salmon', label='Completed Stories')
plt.xticks(rotation=45)
plt.xlabel('Component')
plt.ylabel('Number of Stories')
plt.title('Total Stories vs. Completed Stories per Component')
plt.legend()
plt.show()

# Bar Chart of Total Time (Days) for Each Component
plt.figure(figsize=(12, 6))
sns.barplot(x='component', y='total_time (days)', data=data, palette='viridis')
plt.xticks(rotation=45)
plt.xlabel('Component')
plt.ylabel('Total Time (Days)')
plt.title('Total Time (Days) per Component')
plt.show()

# Dependency Relationships as a Directed Graph
plt.figure(figsize=(10, 8))
G = nx.DiGraph()
for i, row in data.iterrows():
    G.add_edge(row['dependency'], row['component'])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000,
        edge_color='gray', font_size=12, font_weight='bold')
plt.title('Dependency Relationships')
plt.show()

# Completion Status (On Time or Not)
data['on_time'] = data['completed_stories'] == data['total_stories']
plt.figure(figsize=(12, 6))
sns.countplot(x='component', hue='on_time', data=data, palette='Set2')
plt.xticks(rotation=45)
plt.xlabel('Component')
plt.ylabel('Count')
plt.title('Completion Status per Component (On Time or Not)')
plt.legend(title='On Time')
plt.show()
