import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import streamlit as st


def train_and_predict(training_file):
    df = pd.read_csv(training_file)
    features = ['pid', 'org_id', 'component', 'total_stories',
                'completed_stories', 'total_time (days)', 'sprint']
    target = 'dependencies'

    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['component']),
            ('num', 'passthrough', ['pid', 'org_id', 'total_stories',
                                    'completed_stories', 'total_time (days)', 'sprint'])
        ]
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestClassifier(n_estimators=100, random_state=42))
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    results = []
    X_test_with_names = X_test.copy()
    X_test_with_names['task_name'] = df.loc[X_test.index, 'task_name']

    for idx, (index, row) in enumerate(X_test_with_names.iterrows()):
        if y_pred[idx] > 0:
            component = row['component']
            component_sprint = row['sprint']
            dependent_sprint = component_sprint + 1
            task_name = row['task_name']
            results.append({
                "Task Name": task_name,
                "Component": component,
                "Sprint": component_sprint,
                "Dependent Sprint": dependent_sprint
            })

    return results


st.title("Dependency Prediction Results")
st.write("Upload a training CSV file to predict dependencies between tasks.")
uploaded_train_file = st.file_uploader("Upload Training CSV", type="csv")

if uploaded_train_file:
    try:
        results = train_and_predict(uploaded_train_file)
        st.write("### Predicted Dependencies:")
        if results:
            st.dataframe(pd.DataFrame(results))
        else:
            st.write("No dependencies predicted.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please make sure the CSV file is correctly formatted.")
