<a name="_ntjzfniahdk5"></a>ProPilot Predictive Risk Analysis

# <a name="_5c93wssf820"></a><a name="_kd3zrz2l2y6a"></a>Requirements

- Primary Requirement - The prediction tool should look at ProPilot’s data and predict the likelihood of a project finishing on time. It should look at the incoming and completed stories and provide a project risk assessment.
- Data - A temporary utility, outside of the tool, must be created in order to generate a small dataset on which the model can train.

Will this tool be deployed inside the propilot app, or will it be standalone?
- Database connectivity - This tool will need to be able to connect to the propilot backend database to obtain the training data, specifically to the tables containing the project details and the story details. The db details should be provided when the tool is configured. 
- Model - The tool should support multiple machine learning models and provide a way to compare their performance and accuracy for a dataset and choose the best option.
- API - The tool should expose its functionalities as an API for UI integration.
- Security - The API should be secured by using the same authentication and authorization as the propilot app.
- Generic - The tool should be usable in any future projects with different datasets, with minimal changes.
- UI/UX - a simple form - field based UI (input boxes), with basic UX design will be provided to get the status of the project. The result displayed will include a risk assessment of the project that is provided by the tool. 
# <a name="_1sjcf5mkg2c5"></a>Use Cases

|Scenario|Response|
| :-: | :-: |
|The progress of the project is continuing in either an increasing trend or continuing trend (such that the time taken for completion is on or before the end date provided)|<p>On Schedule: Yes</p><p>Status: Green</p>|
|The progress of the project is continuing in a downward trend, but is still projected to be finished by the required date.|<p>On Schedule: Yes</p><p>Status: Amber</p>|
|The progress of the project has slowed down to a point where continuing with the same speed would not allow the project to be finished, or the release date has been preponed such that the current progress is not enough.|<p>On Schedule: No</p><p>Status: Red</p>|


# <a name="_fw2gu567jz3t"></a>Design
## <a name="_uu6mk0n20ywk"></a>Data Model
The tool will make predictions based on the data in the following tables:

- Projects table - For reading the start and end dates of a project.
- Stories table - The tool will predict based on the rate of story completion
- Audit table - For reading the completion date of a story.

Note:

- Data is not deleted from the table when the project is completed. Hence, this historical data will be used to train the model.
- All stories are considered to be of equal weightage. 

  As a future enhancement, we can support story points in order to clearly quantify the complexity of each story.  We cannot rely on story point completion as a consistent  way of quantifying progress as not every team would do storypointing.
## <a name="_4z1yb5l98i8j"></a>Data Generator
Currently, the propilot database does not have enough data to train a model on. So, a tool is needed in order to generate the training and testing data. This can be a temporary measure until sufficient organic data is available.

The tool should generate data for use cases like:

- Average case 1 - Project with 10 stories that is completed in 3 months
- Average case 2 - Project that is in progress with some stories completed
- Outlier 1 - Project with 2 stories that is completed in 3 months
- Outlier 2 - Project with 30 stories that is completed in 3 months

Next step:

Explore the sample datasets on kaggle further to see if any related datasets can be found and reused.
## <a name="_78jeitn6llr5"></a>Prediction Backend
Language - Python (as it has the best suite for machine learning tasks).

High level tasks:

- Data transformation as needed
- Create wrapper class for the various models
- Train and generate the models
- Test the models using a confusion matrix
- Select the best model for the dataset

API:

- GET /rest/v1/prediction?projectid=<> - This will use the model that was selected above, and use it to return a prediction for the requested project.
- POST /rest/v1/train - Use the data in the propilot database to retrain itself.

## <a name="_dowscdiwpv25"></a>Frontend
To access the tool, a dashboard widget should be added in the propilot app, preferably in the same place as where the user can see all the current projects.

Future Enhancement:

UI can be a dashboard with a natural language-based query tool. For example, a query can be in the form *“Do you think project ‘x’ can be finished on time?”*, and the tool will return the requested data in both textual and visual (graphical) form. For example, an infographic describing the zone (green, amber or red) and the progress trend (a graph of the amount of tasks completed in a day vs. the number of days since the project started) can be displayed.

