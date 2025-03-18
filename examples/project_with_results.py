import pandas as pd
from debiai_data_provider import DebiAIProject, DataProvider

# This file is an example of a simple project
# exposed with the DebiAI Data Provider python module.
# It shows how to define a project structure,
# provide project data and model results,
# and define actions that can be performed on the project.

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

# Project model results
MODEL_RESULTS = pd.DataFrame(
    {
        "sample_id": ["image-1", "image-1", "image-2", "image-2"],
        "model": ["model_1", "model_2", "model_1", "model_2"],
        "prediction": [10, 12, 8, 5],
        "confidence": [0.8, 0.9, 0.7, 0.6],
        "error": [2, 4, 1, -2],
        "error_abs": [2, 4, 1, 2],
    }
)


# Define a class that inherits from DebiAIProject
# This class will be used to define the project structure
# to gather the project samples and model results
# and to define the actions that can be performed on the project
class MyProjectWithResults(DebiAIProject):
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

    def get_results_structure(self) -> dict:
        # This function will be called when the user
        # opens the project in the DebiAI interface
        # It is required if you plan to analyze model results

        return {
            "prediction": {
                "type": "number",
            },
            "confidence": {
                "type": "number",
            },
            "error": {
                "type": "number",
                "group": "error",
            },
            "error_abs": {
                "type": "number",
                "group": "error",
            },
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

    # Project model results
    def get_models(self) -> list[dict]:
        # This function will be called when DebiAI
        # ask the user to select a model to analyze the results
        # The function should return the list of models
        # that have been evaluated on the project

        unique_models = MODEL_RESULTS["model"].unique()

        models_data = []
        for model in unique_models:
            nb_results = len(MODEL_RESULTS[MODEL_RESULTS["model"] == model])

            models_data.append(
                {
                    "id": model,
                    "name": model,
                    "nb_results": nb_results,
                }
            )

        return models_data

    def get_model_evaluated_data_id_list(self, model_id: str) -> list[str]:
        # This function will be called when the user
        # wants to analyze the results of a specific model
        # The function should return the list of samples ids
        # that have been evaluated by the model

        unique_models = MODEL_RESULTS["model"].unique()

        if model_id not in unique_models:
            raise ValueError(f"Model {model_id} not found")

        return MODEL_RESULTS[MODEL_RESULTS["model"] == model_id]["sample_id"].tolist()

    def get_model_results(self, model_id: str, samples_ids: list[str]) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze the results of a specific model
        # The function should return a pandas DataFrame
        # containing the results of the model corresponding
        # to the samples_ids provided

        # Filter the results
        model_inferences = MODEL_RESULTS[
            (MODEL_RESULTS["model"] == model_id)
            & (MODEL_RESULTS["sample_id"].isin(samples_ids))
        ]

        return model_inferences

    # Project actions
    def delete_project(self):
        # This function will be called when the user
        # wants to delete the project
        print("Delete project called")
        raise NotImplementedError


provider = DataProvider()

provider.add_project(MyProjectWithResults())

# Finally, start the server
provider.start_server()
