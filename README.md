# DebiAI Data Provider Python module

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This [DebiAI](https://debiai.irt-systemx.fr/) Data Provider Python module allows you to easily deploy your own data-provider through the data-provider API.

A data-provider allows you to provide data to DebiAI so that no duplication of data is needed.

[DebiAI Data-providers documentation](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/)

## Getting started

### Installation

Install `debiai_data_provider` with pip:

```bash
pip install debiai_data_provider
```

### Usage example

Find out how to use the DebiAI Data Provider Python module in the [examples](examples) folder:

- [simple_project.py](examples/simple_project.py) shows how to create a simple data-provider with a project

#### Provide project metadata

Create a Python Class representing your project:

```python
from debiai_data_provider import DebiAIProject, DataProvider


class MyProject(DebiAIProject):
    creation_date = "2024-01-01"

    def get_structure(self) -> dict:
        # This function will be called when the user
        # opens the project in the DebiAI interface
        # It serves to classify the project data structure

        return {
            "Data ID": {"type": "text", "category": "id"},
            "My context 1": {"type": "text", "category": "context"},
            "My context 2": {"type": "number", "category": "context"},
            "My groundtruth 1": {"type": "number", "category": "groundtruth"},
        }

    def get_data(self) -> pd.DataFrame:
        # This function will be called when the user
        # wants to analyze data from your project
        samples_df = pd.DataFrame(
            {
                "Data ID": ["image-1", "image-2", "image-3"],
                "My context 1": ["A", "B", "C"],
                "My context 2": [0.28, 0.388, 0.5],
                "My groundtruth 1": [8, 7, 19],
            }
        )

        return samples_df


my_project = MyProject()
```

#### Start the server and link your data-provider with DebiAI

Then, create an DataProvider object and add your project to it:

```python
provider = DataProvider()

provider.add_project(my_project)

# Finally, start the server
provider.start_server()
```

Run the Python file and your project is now available through the DebiAI Data Provider API!

To link your data-provider with DebiAI, you can follow our [Creation of a data provider guide](https://debiai.irt-systemx.fr/dataInsertion/dataProviders/quickStart.html)

#### Provide project model results

To provide your model results to DebiAI, add the following method to your project class:

```python
class MyProject(DebiAIProject):

    # Project metadata
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
```

## Roadmap

- [ ] Publish to Pypi
- [ ] Provide project data
  - [x] Provide project metadata
  - [x] Provide project samples
  - [x] Provide project models & model results
  - [ ] Provide project selections
- [ ] Make available project interactions
  - [x] Project deletion
  - [ ] Model deletion
  - [ ] Selection creation
  - [ ] Selection deletion
- [ ] High level data-providers
  - [ ] CSV data-provider
  - [ ] Json data-provider
- [ ] Start DebiAI along with the data-provider
- [ ] LLM improved data-provider for auto configuration

---

<p align="center">
  DebiAI is developed by 
  <a href="https://www.irt-systemx.fr/" title="IRT SystemX">
   <img src="https://www.irt-systemx.fr/wp-content/uploads/2013/03/system-x-logo.jpeg"  height="70">
  </a>
  And is integrated in 
  <a href="https://www.confiance.ai/" title="Confiance.ai">
   <img src="https://pbs.twimg.com/profile_images/1443838558549258264/EvWlv1Vq_400x400.jpg"  height="70">
  </a>
</p>

---
