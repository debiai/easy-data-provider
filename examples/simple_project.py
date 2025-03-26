import pandas as pd
from debiai_data_provider import DebiAIProject, DataProvider

# This file is an example of a simple project
# exposed with the DebiAI Data Provider python module.
# It shows how to define a project structure,
# provide project data and define actions
# that can be performed on the project.

# Project data
PROJECT_DATA = pd.DataFrame(
    {
        "Data ID": ["image-1", "image-2", "image-3"],
        "My context 1": ["A", "B", "C"],
        "My context 2": [0.28, 0.388, 0.5],
        "My groundtruth 1": [8, 7, 19],
        "input": [100, 200, 128],
    }
)


# Define a class that inherits from DebiAIProject
# This class will be used to define the project structure
# to gather the project samples and model results
# and to define the actions that can be performed on the project
class MyProject(DebiAIProject):
    creation_date = "2024-01-01"

    # Project metadata
    def get_structure(self) -> dict:
        # This function will be called when the user
        # opens the project in the DebiAI interface
        # It serves to classify the project data structure

        return {
            "My context 1": {"type": "text", "category": "context", "group": "context"},
            "My context 2": {
                "type": "number",
                "category": "context",
                "group": "context",
            },
            "My groundtruth 1": {"type": "number", "category": "groundtruth"},
        }

    # Project samples
    def get_nb_samples(self) -> int:
        # This function returns the number of samples in the project
        return len(PROJECT_DATA)

    def get_samples_ids(self) -> list[str]:
        # This function returns the list of samples ids
        return PROJECT_DATA["Data ID"].tolist()

    def get_data(self, samples_ids: list[str]) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project

        # The function should return a pandas DataFrame
        # containing the data corresponding to the samples_ids

        return PROJECT_DATA[PROJECT_DATA["Data ID"].isin(samples_ids)]

    # Project actions
    def delete_project(self):
        # This function will be called when the user
        # wants to delete the project
        print("Delete project called")
        raise NotImplementedError


# You can define multiple projects in the same file
class MyProject2(DebiAIProject):
    pass


provider = DataProvider()

provider.add_project(MyProject())
provider.add_project(MyProject2())

# Finally, start the server
provider.start_server(auto_reload=True)
